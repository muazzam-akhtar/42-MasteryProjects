import psycopg2

dbname = "piscineds"
user = "makhtar"
password = "mysecretpassword"
host = "postgres"
port = "5432"

try:
    with open("remove_duplicates.sql", "r") as sql_file:
        sql_script = sql_file.read()
    print("\033[1;32mSQL code has been imported!\033[0;39m")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("\033[1;32mConnected to Postgres!\033[0;39m")
    cursor = conn.cursor()
    cursor.execute(sql_script)
    print("\033[1;32mSQL script executed successfully!")
    print("Removed all the duplicates from the table.\033[0;39m")
    conn.commit()

except Exception as e:
    print(f"\033[1;31mError: {str(e)}\033[0;39m")

finally:
    cursor.close()
    conn.close()
