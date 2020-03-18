# BCBS Coding Challenge
This is python package to find the best rated restaurant in Yelp that is
located within 20 meters of the next 7 subsequent bus stops given a bus route,
direction and first next stop id.

## Versions
This package was built with python 3.7 and the requests package

## How To Use
```python
import hungry

fbr = hungry.FindBestResturants(
  yelp_key=<your yelp key>
  cta_key=<your cta key>
)

best_restaurant = fbr.search_by_route(
    route_id="29",
    direction="northbound",
    next_stop_id="1438"
)
```
### The output
```
{'7vsOVA4wrHP6f3DMQdD8og': {'id': '7vsOVA4wrHP6f3DMQdD8og',
  'alias': 'volare-ristorante-italiano-chicago',
  'name': 'Volare Ristorante Italiano',
  'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/H7fhBsj5Fmw1LY3nP6UMrA/o.jpg',
  'is_closed': False,
  'url': 'https://www.yelp.com/biz/volare-ristorante-italiano-chicago?adjust_creative=BT6TqGwLBGtjLRKOJdpQlg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=BT6TqGwLBGtjLRKOJdpQlg',
  'review_count': 2091,
  'categories': [{'alias': 'italian', 'title': 'Italian'}],
  'rating': 4.0,
  'coordinates': {'latitude': 41.8915901798304,
   'longitude': -87.6225186472213},
  'transactions': ['delivery', 'restaurant_reservation', 'pickup'],
  'price': '$$',
  'location': {'address1': '201 E Grand Ave',
   'address2': '',
   'address3': '',
   'city': 'Chicago',
   'zip_code': '60611',
   'country': 'US',
   'state': 'IL',
   'display_address': ['201 E Grand Ave', 'Chicago, IL 60611']},
  'phone': '+13124109900',
  'display_phone': '(312) 410-9900',
  'distance': 10.616120022366152}}
```
