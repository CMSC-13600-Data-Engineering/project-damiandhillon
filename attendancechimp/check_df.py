import pandas as pd
#adjust the courseid with the new course id when running test2.py 
df = pd.read_json('http://localhost:8000/app/getUploads?course=23')
df2 = pd.read_json('http://localhost:8000/app/getUploads?course=24')

print(df)
print(df2)