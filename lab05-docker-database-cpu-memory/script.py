
import xml.etree.ElementTree as ET

tree = ET.parse('config.xml')
root = tree.getroot()

db_host = root.find('./database/host').text
db_user = root.find('./database/user').text

print(f"Connecting to database at {db_host} with user {db_user}")
