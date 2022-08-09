def create_table(db, table_name="jobs"):
    try:
        if table_name in [table.name for table in db.tables.all()]:
            table = db.Table(table_name)
            table.delete()
            table.wait_until_not_exists()
        table = db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

        return table
    except Exception as e:
        print(e)
