from typing import List, Optional

from bson import ObjectId
from db.Idatabase import BaseRepository, IContactRepository
from db.exceptions import OperationFailed, RecordNotFound
from models import Contact, ContactUpdate
from starlette.concurrency import run_in_threadpool


class MongoContactRepository(BaseRepository, IContactRepository):
    def __init__(self, connector):
        super().__init__(connector)
        self.collection = connector.get_collection("contacts")

    def _map_document(self, doc: dict) -> Contact:
        if "_id" in doc:
            doc["id"] = doc["_id"]
            doc.pop("_id")
        return Contact(**doc)

    def _create_sync(self, contact: Contact) -> str:
        contact_dict = contact.model_dump(exclude={"id"})
        try:
            if not self._get_by_phone_number_sync(contact.phone_number):
                result = self.collection.insert_one(contact_dict)
                return str(result.inserted_id)

        except Exception as e:
            raise OperationFailed(f"Create failed in Mongo: {e}")

    def _get_all_sync(self) -> List[Contact]:
        try:
            cursor = self.collection.find()
            return [self._map_document(doc) for doc in cursor]
        except Exception as e:
            raise OperationFailed(f"Get all failed: {e}")

    def _get_by_id_sync(self, contact_id: ObjectId) -> Optional[Contact]:
        try:
            doc = self.collection.find_one({"_id": contact_id})
            if doc:
                return Contact(**doc)
            return None
        except Exception as e:
            raise OperationFailed(f"Get by id failed: {e}")

    def _get_by_phone_number_sync(self, phone_number: str) -> Optional[Contact]:
        try:
            doc = self.collection.find_one({"phone_number": phone_number})
            if doc:
                return Contact(**doc)
            return None
        except Exception as e:
            raise OperationFailed(f"Get by phone_number failed: {e}")

    def _update_sync(self, contact_id: ObjectId, contact_update: ContactUpdate) -> None:
        update_data = contact_update.model_dump(exclude_unset=True)

        if not update_data:
            return

        try:
            result = self.collection.update_one(
                {"_id": contact_id},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                raise RecordNotFound(f"Contact {contact_id} not found for update")

        except Exception as e:
            raise OperationFailed(f"Update failed: {e}")

    def _delete_sync(self, contact_id: ObjectId) -> None:
        try:
            result = self.collection.delete_one({"_id": contact_id})
            if result.deleted_count:
                raise RecordNotFound(f"Contact {contact_id} not found for delete")
        except Exception as e:
            raise OperationFailed(f"Delete failed: {e}")

    async def create(self, contact: Contact) -> str:
        return await run_in_threadpool(self._create_sync, contact)

    async def get_all(self) -> List[Contact]:
        return await run_in_threadpool(self._get_all_sync)

    async def get_by_id(self, contact_id: ObjectId) -> Optional[Contact]:
        return await run_in_threadpool(self._get_by_id_sync, contact_id)

    async def update(self, contact_id: ObjectId, contact: ContactUpdate) -> None:
        await run_in_threadpool(self._update_sync, contact_id, contact)

    async def delete(self, contact_id: ObjectId) -> None:
        await run_in_threadpool(self._delete_sync, contact_id)
