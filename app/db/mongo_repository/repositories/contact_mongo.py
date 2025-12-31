from typing import List, Optional

from bson import ObjectId
from db.Idatabase import BaseRepository, IContactRepository
from db.exceptions import OperationFailed, RecordNotFound
from models import Contact, ContactUpdate


class MongoContactRepository(BaseRepository, IContactRepository):
    """MongoDB implementation of the IContactRepository interface."""

    def __init__(self, connector):
        """Initializes the MongoContactRepository with a MongoDB connector."""
        super().__init__(connector)
        self.collection = connector.get_collection("contacts")

    def _map_document(self, doc: dict) -> dict:
        """Maps a MongoDB document to a Contact model."""
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
            doc.pop("_id")
        return doc

    def _get_by_phone_number_sync(self, phone_number: str) -> Optional[Contact]:
        """Synchronous helper to get a contact by phone number."""
        try:
            doc = self.collection.find_one({"phone_number": phone_number})
            if doc:
                return Contact(**doc)
            return None
        except Exception as e:
            raise OperationFailed(f"Get by phone_number failed: {e}")

    def create(self, contact: Contact) -> str | None:
        """Creates a new contact in the collection."""
        contact_dict = contact.model_dump(exclude={"id"})
        try:
            if not self._get_by_phone_number_sync(contact.phone_number):
                result = self.collection.insert_one(contact_dict)
                return str(result.inserted_id)
        except Exception as e:
            raise OperationFailed(f"Create failed in Mongo: {e}")

    def get_all(self) -> List[Contact] | None:
        """Retrieves all contacts from the collection."""
        try:
            cursor = self.collection.find()
            return [self._map_document(doc) for doc in cursor]
        except Exception as e:
            raise OperationFailed(f"Get all failed: {e}")

    def get_by_id(self, contact_id: str) -> Optional[Contact]:
        """Retrieves a contact by its ID."""
        try:
            doc = self.collection.find_one({"_id": ObjectId(contact_id)})
            if doc:
                return Contact(**doc)
            return None
        except Exception as e:
            raise OperationFailed(f"Get by id failed: {e}")

    def update(self, contact_id: str, contact_update: ContactUpdate) -> None:
        """Updates a contact by its ID."""
        update_data = contact_update.model_dump(exclude_unset=True)
        if not update_data:
            return
        try:
            print("Updating contact:", contact_id, contact_update)
            result = self.collection.update_one(
                {"_id": ObjectId(contact_id)},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                raise RecordNotFound(f"Contact {contact_id} not found for update")
        except Exception as e:
            raise OperationFailed(f"Update failed: {e}")

    def delete(self, contact_id: str) -> None:
        """Deletes a contact by its ID."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(contact_id)})
            if result.deleted_count == 0:
                raise RecordNotFound(f"Contact {contact_id} not found for delete")
        except Exception as e:
            raise OperationFailed(f"Delete failed: {e}")
