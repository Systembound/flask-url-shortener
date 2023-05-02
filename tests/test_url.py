from flask import url_for

from api.models import api as api_models


def test_url_shorten_manager(client, db, user, admin_headers):
    response = client.json(url_for('api.url'), headers=admin_headers)
    assert response.status_code == 400
    # assert response returned
    # convert it into json, validate response has url with error
    assert response.get_json()['url'][0] == 'Missing data for required field.'

    # send response with correct request payload
    response = client.json(url_for('api.url'), headers=admin_headers, data={
        'url': 'https://www.google.com',
    })
    assert response.status_code == 201

    # check if data is saved in db
    url_db_instance = db.session.query(api_models.Url).filter_by(id=1).first()
    assert url_db_instance.url == 'https://www.google.com'
    assert url_db_instance.new is not None

    # now, visit the url and check if it redirects to the original url
    response = client.get(url_for('shortcuts.short_url_visits', short_url_id=url_db_instance.new),)
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://www.google.com'

    # check if hits is incremented
    assert url_db_instance.hits == 1

    # get detailed visits of the url
    response = client.get(url_for('api.url', short_url_id=url_db_instance.new), headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()['hits'] == 1
    assert response.get_json()['url'] == 'https://www.google.com'
