#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
from tweepy.error import TweepError
import json
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_tweet_url_from_status(status):
	return "https://twitter.com/{0}/status/{1}".format(status.user.screen_name, status.id)

class Listener(tweepy.StreamListener):
	def on_status(self, status):
		status.created_at += datetime.timedelta(hours=9)

		# ** favo when reply
		if str(status.in_reply_to_screen_name) == client_info["screen_name"]:
			if str(status.user.screen_name) == client_info["screen_name"]:
				# exclude self reply.
				pass
			else:
				print("receive reply: " + str(datetime.datetime.today()))
				try:
					api.create_favorite(status.id)
				except TweepError as err:
					pp.pprint(err)
				return True

		# ** favo when retweet
		if hasattr(status, "retweeted_status"):
			print("receive retweet: " + str(datetime.datetime.today()))
			try:
				api.create_favorite(status.id)
			except TweepError as err:
				pp.pprint(err)
			return True

		# ** reply when mention ("@" tweet)
		for user_mention in status.entities['user_mentions']:
			#print("receive mention: {0} {1}".format(status.user.screen_name, str(datetime.datetime.today())))
			#pp.pprint(user_mention)

			if str(status.user.screen_name) == client_info["screen_name"]:
				# exclude self mention.
				pass
			else:
				#print("receive mention: " + str(datetime.datetime.today()))

				# ** retweet
				#try:
				#	api.retweet(status.id)
				#except TweepError as err:
				#	pp.pprint(err)
					#return False

				# ** quote tweet(ja:`引用ツイート`)
				try:
					tweet_url = get_tweet_url_from_status(status)
					tweet = "Quite tweet test!\n{0}".format(tweet_url)
					api.update_status(status=tweet, in_reply_to_status_id=status.id)
				except TweepError as err:
					pp.pprint(err)

				# ** reply
				try:
					tweet = "@{0} Hello!\n {1}".format(status.user.screen_name, str(datetime.datetime.today()))
					api.update_status(status=tweet, in_reply_to_status_id=status.id)
				except TweepError as err:
					pp.pprint(err)
					#return False
			return True

		return True

	def on_error(self, status_code):
		print('Error code:' + str(status_code))
		return True

	def on_timeout(self):
		print('Timeout error')
		return True


# screen_name and access keys
f = open('client.json', 'r')
client_info = json.load(f)
f.close()

# auth
auth = tweepy.OAuthHandler(client_info["consumer_key"], client_info["consumer_secret"])
auth.set_access_token(client_info["access_token"], client_info["access_secret"])
api = tweepy.API(auth)

# tweeet when bot startup
api.update_status("Hello. : " + str(datetime.datetime.today()))

# stream
listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.userstream()

