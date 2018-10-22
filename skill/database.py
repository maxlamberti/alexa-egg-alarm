import time
import boto3
import logging
import decimal
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class DatabaseConnector:

	def __init__(self):
		dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
		self.table = dynamodb.Table('egg-timer')

	def get_user(self, alexa_id):
		try:
			response = self.table.get_item(Key={'alexa_id': alexa_id})
			item = response.get('Item', {})
		except ClientError:
			logger.error("Failed getting user data from table for user %s", alexa_id, exc_info=True)
			item = {}

		# decimals not json serializable --> convert to float
		for k, v in item.items():
			if isinstance(v, decimal.Decimal):
				item[k] = float(v)

		return item

	def initialize_user(self, alexa_id, locale):

		item = {
			'alexa_id': alexa_id,
			'locale': locale,
			'last_visit': int(time.time()),
			'num_visits': 0
		}

		try:
			self.table.put_item(Item=item)
		except ClientError:
			logger.error("Failed initializing data for user %s", alexa_id, exc_info=True)

		return item

	def update_visit(self, alexa_id):
		try:
			_ = self.table.update_item(
				Key={'alexa_id': alexa_id},
				UpdateExpression="SET num_visits = num_visits + :increment, last_visit = :time_now",
				ExpressionAttributeValues={':increment': 1, ':time_now': int(time.time())}
			)
		except ClientError:
			logger.error("Failed incrementing table for user %s", alexa_id, exc_info=True)

	def set_boiling_scale_preference(self, alexa_id, boiling_scale):
		try:
			self.table.update_item(
				Key={'alexa_id': alexa_id},
				UpdateExpression="SET default_boiling_scale = :val",
				ExpressionAttributeValues={':val': boiling_scale}
			)
		except ClientError:
			logger.error("Failed setting boiling scale preference for user %s", alexa_id, exc_info=True)

	def remove_boiling_scale_preference(self, alexa_id):
		try:
			self.table.update_item(
				Key={'alexa_id': alexa_id},
				UpdateExpression="REMOVE default_boiling_scale"
			)
		except ClientError:
			logger.error("Failed removing default boiling scale for user %s", alexa_id, exc_info=True)

	def set_last_boiling_scale(self, alexa_id, boiling_scale):
		try:
			self.table.update_item(
				Key={'alexa_id': alexa_id},
				UpdateExpression="SET last_boiling_scale = :val",
				ExpressionAttributeValues={':val': boiling_scale}
			)
		except ClientError:
			logger.error("Failed saving boiling scale for user %s", alexa_id, exc_info=True)


if __name__ == '__main__':

	test_locale = 'en-GB'
	test_alexa_id = (
		"amzn1.ask.account.AFRET2RY4UHTI5N7FJTZQ3XDEVZMLZ47UZWZ6DFVPNDJLVZKDDMOVGR23QUKQMM4BK723EBA2WN3GUBCMN7A34AXII"
		"OCN4TWMUYLV2GGCPLGBHZPZ7FXEDF5VWTAY555VYKHRJAKSLYH5TDYJKEAAOXP7GCRENWGYSH43VRH4DNWSJ3PBU3MYKMO6ZN5MFRA5BYM3E"
		"WEYHACVQI"
	)

	db = DatabaseConnector()
	db.initialize_user(test_alexa_id, test_locale)
	db.set_boiling_scale_preference(test_alexa_id, 'soft')
	print(db.get_user(test_alexa_id))
