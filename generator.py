import random
import uuid
from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials, firestore, storage

from constant import constant

# Use a service account
cred = credentials.Certificate(
    './local/paeparo-firebase-adminsdk-c05v5-18426933bc.json')  # replace with your serviceAccount.json
firebase_admin.initialize_app(cred, {
    'storageBucket': 'paeparo.appspot.com'  # replace with your app's bucket name
})
db = firestore.client()
bucket = storage.bucket()


def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


def upload_image_to_firebase(user_id, post_id, image_path):
    blob = bucket.blob(f'images/{user_id}/{post_id}/{uuid.uuid4()}')
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url


def generate_trip_and_post(regions, titles, users, descriptions, tags, sample_images):
    trip = {}
    trip['region'] = random.choice(regions)
    trip['name'] = random.choice(titles[trip['region']])
    trip['status'] = random.choice(["PLANNING", "ONGOING", "FINISHED"])
    start_date = random_date(datetime(2023, 4, 1), datetime(2023, 10, 31))
    end_date = start_date + timedelta(days=random.randint(2, 5))
    trip['start_date'] = start_date
    trip['end_date'] = end_date
    trip['budget'] = random.randint(100000, 3000000)
    trip['members'] = random.sample(users, random.randint(1, 2))
    trip['invitations'] = random.sample([user for user in users if user not in trip['members']], random.randint(1, 2))

    trip_ref = db.collection('trips').document()
    trip['trip_id'] = trip_ref.id
    trip_ref.set(trip)

    if trip['status'] == 'FINISHED':
        post = {}
        post['trip_id'] = trip['trip_id']
        post['user_id'] = trip['members'][0]
        post['region'] = trip['region']
        post['title'] = trip['name']
        post['description'] = random.choice(descriptions[trip['region']])
        post['created_at'] = end_date + timedelta(hours=random.randint(18, 23))
        post['likes'] = random.randint(1, 1000)
        post['tags'] = random.sample(tags, 5)
        post['images'] = [upload_image_to_firebase(post['user_id'], trip['trip_id'], img) for img in
                          random.sample(sample_images[trip['region']], 2)]

        post_ref = db.collection('posts').document()
        post['post_id'] = post_ref.id
        post_ref.set(post)

        return trip, post

    return trip, None


for _ in range(20):
    trip, post = generate_trip_and_post(constant.regions, constant.titles, constant.users, constant.descriptions,
                                        constant.tags, constant.images)
    print(trip)
    if post:
        print(post)
