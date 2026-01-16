import pytest
from fastapi import HTTPException
from app.models.ads import Ad


def test_create_ad_sets_owner_and_persists(service, db_session, create_payload):
    payload = create_payload(title="Phone", description="nice", price=100, category=["phone"])
    ad = service.create_ad(payload, current_user_id=10)

    assert ad.id is not None
    assert ad.owner_id == 10
    assert ad.title == "Phone"

    in_db = db_session.query(Ad).filter(Ad.id == ad.id).first()
    assert in_db is not None


def test_get_ad_or_404_not_found(service):
    with pytest.raises(HTTPException) as e:
        service.get_ad_or_404(999999)
    assert e.value.status_code == 404


def test_update_ad_forbidden_if_not_owner(service, create_payload, update_payload):
    ad = service.create_ad(
        create_payload(title="old", description="d", price=50, category=["x"]),
        current_user_id=1
    )

    with pytest.raises(HTTPException) as e:
        service.update_ad(ad.id, update_payload(title="new"), current_user_id=2)

    assert e.value.status_code == 403


def test_update_ad_updates_only_given_fields(service, create_payload, update_payload):
    ad = service.create_ad(
        create_payload(title="old", description="d", price=50, category=["x"]),
        current_user_id=1
    )

    updated = service.update_ad(ad.id, update_payload(title="new"), current_user_id=1)

    assert updated.title == "new"
    assert updated.price == 50


def test_delete_ad_forbidden_if_not_owner(service, db_session, create_payload):
    ad = service.create_ad(
        create_payload(title="x", description="d", price=1, category=["x"]),
        current_user_id=1
    )

    with pytest.raises(HTTPException) as e:
        service.delete_ad(ad.id, current_user_id=999)

    assert e.value.status_code == 403
    assert db_session.query(Ad).filter(Ad.id == ad.id).first() is not None


def test_delete_ad_removes_record(service, db_session, create_payload):
    ad = service.create_ad(
        create_payload(title="x", description="d", price=1, category=["x"]),
        current_user_id=1
    )

    service.delete_ad(ad.id, current_user_id=1)

    assert db_session.query(Ad).filter(Ad.id == ad.id).first() is None


def test_list_ads_returns_all(service, create_payload):
    service.create_ad(create_payload(title="a", description="d", price=1, category=["a"]), current_user_id=1)
    service.create_ad(create_payload(title="b", description="d", price=2, category=["b"]), current_user_id=2)

    ads = service.list_ads()
    assert len(ads) == 2
