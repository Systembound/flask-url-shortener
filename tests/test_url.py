from flask import url_for


def test_url_shorten_manager(client, db, user, admin_headers):
    # test 404
    rep = client.get(url_for('api.url'), headers=admin_headers)
    breakpoint()
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_url = url_for('api.user_by_id', user_id=user.id)
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active
