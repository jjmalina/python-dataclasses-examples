set -e
curl -v -XPOST -H 'Content-Type: application/json' -d '{"first_name":"Jeremiah","last_name":"Malina"}' http://localhost:5000/people | json_pp


curl -v -XPUT -H 'Content-Type: application/json' -d '{"email":"jereremiah.malina@welcomesoftware.com"}' http://localhost:5000/people/c2509e73b9424563b112f146f776f680 | json_pp

curl -v -XPUT -H 'Content-Type: application/json' -d '{"id":"c2509e73b9424563b112f146f776f680","created_timestamp":"2021-07-20T15:55:16.162001","first_name":"Jeremiah","last_name":"Malina","email":"jereremiah.malina@welcomesoftware.com"}' http://localhost:5000/people/c2509e73b9424563b112f146f776f680 | json_pp


curl -v -XDELETE http://localhost:5000/people/c2509e73b9424563b112f146f776f680
