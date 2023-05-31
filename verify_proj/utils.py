import os
from twilio.rest import Client
import logging

#Your account sid và auth token form twilio.com/console
#and set the environment variables. See http://twil.io/secure

account_sid = 'AC8787a74a8bb233965995b8a33b1249fb'
auth_token = 'd3330a5731d00ecbd914a8082a474113'
verify_sid= 'VAebde1c4c9daa2e5fabd7d469b2adbab1'
client = Client(account_sid, auth_token)

"""
Config logging
"""
logging.basicConfig(filename="./log.txt")
client.http_client.logger.setLevel(logging.ERROR)


def send_sms(user_code, phone_number):
    try:
      message = client.messages.create(
                              body=f'Hi! Your user and verification code is {user_code}',
                              from_='+13156231233',                
                              to=f'{phone_number}'
                            )
      print(message.sid)
    except Exception as e:
       logging.error(e)

def generate_otp(verified_number):
      verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
      return verification 

def verify_otp(otp_code, verified_number):
      verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
      return verification_check.status