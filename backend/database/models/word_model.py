from peewee import TextField, ForeignKeyField, IntegerField
from database import connection
from database.models.analysis_model import Analysis


class Word(connection.BaseModel):
    text = TextField(null=False)
    quantity = IntegerField(null=False)
    analysis = ForeignKeyField(column_name="analysis_id", field="id", model=Analysis)

    class Meta:
        table_name = "word"

def insert_many(words):
    try:
        Word.insert_many(words).execute()
    except Exception as ex:
        raise ex

def get_by_analysis(analysis_id):
    try:
        return (
            Word.select()
            .where(Word.analysis == analysis_id)
            .order_by(Word.quantity.desc())
            .limit(40)
            .execute()
        )
    except Word.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
