from src.accounts.models import Account, Transaction
from src.app.utils.base_repository import BaseRepo


class AccountRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(Account)

    def create(self, account_dict: dict) -> Account:
        account = Account(**account_dict)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_balance(self, user_id: int):
        return self.base_query.filter(Account.user_id == user_id).first()

    def update(self, account: Account) -> Account:
        self.db.commit()
        self.db.refresh(account)
        return account


class TrasactionRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(Transaction)

    def create(self, transfer_dict: dict) -> Transaction:
        transfer = Transaction(**transfer_dict)
        self.db.add(transfer)

        self.db.commit()
        self.db.refresh(transfer)
        return transfer

    def get(self):
        return self.base_query.all()

    def get_by_tranzact_id(self, transact_id: str):
        return self.base_query.filter(Transaction.tranzact_id == transact_id).first()

    def update(self, transfer: Transaction) -> Transaction:
        self.db.commit()
        self.db.refresh(transfer)
        return transfer

    def delete(self, transfer: Transaction):
        self.db.delete(transfer)
        self.db.commit()


account_repo = AccountRepo()

transaction_repo = TrasactionRepo()
