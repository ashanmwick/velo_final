import googlemaps
#-------User Management---------#
#Check user by User ID
def checkUserId(db, table, id):
    data = db.child(table).get().val()
    return id in data.keys()


#function to retrive subsessions (func 1)----Sachini
def retreivesubsessions(db, table, id, date, session):   
  summary = db.child(table).child(id).child(date).child(session).get()
  result_dict = {}
  for item in summary.each():
    if item.key() == "alt":
      break
    result_dict[item.key()] = item.val()
  #print(result_dict)

  return result_dict




#function to retrive only time by given date(func 4)----Sachini
def retrieve_sessions_with_time(db, table, id, date):
  summary = db.child(table).child(id).child(date).get().val()
  result_dict = {}
  for key, value in summary.items():
    if key != "date":
      result_dict[key] = value["strt"]
  print(result_dict)
  return result_dict

#function to retrive only date by given id(func 3)----Sachini    
def retreivedate(db, table, id):
    summary = db.child(table).child(id).get()
    result_dict = {}

    if summary.val() is None:  # Check if the data is None
        result_dict['error'] = 'Please input your data correctly'
    else:
        for item in summary.each():
            result_dict[item.key()] = item.val().get("date")

    return result_dict



#------------Sumarrlization function starts here----Sachini----#
#find  the average of environment temperature
def temp(id, date, session):
  data = db.child("history").child(id).child(date).child(session).get()
  data_dict = data.val()
  sum = 0
  a = len(list(data_dict.values()))
  for count in range(0, a - 3):
    sum = sum + list(data_dict.values())[count]["envTemp"]
  result = sum / (a - 3)
  print(result)
  db.child("history").child(id).child(date).child(session).update(
    {"envtemp": result})


#find  the average of heartrate
def heart_rate(db,id, date, session):
  data = db.child("history").child(id).child(date).child(session).get()
  data_dict = data.val()
  sum = 0
  a = len(list(data_dict.values()))
  for count in range(0, a - 4):
    sum = sum + list(data_dict.values())[count]["hrtRate"]
  result = sum / (a - 4)
  print(result)
  db.child("history").child(id).child(date).child(session).update(
    {"heart rate": result})


#find  the average of speed
def speed(db,id, date, session):
  data = db.child("history").child(id).child(date).child(session).get()
  data_dict = data.val()
  sum = 0
  a = len(list(data_dict.values()))
  for count in range(0, a - 5):
    sum = sum + list(data_dict.values())[count]["speed"]
  result = sum / (a - 5)
  print(result)
  db.child("history").child(id).child(date).child(session).update(
    {"speed": result})


#find  the average of humidity
def humidity(db,id, date, session):
  data = db.child("history").child(id).child(date).child(session).get()
  data_dict = data.val()
  sum = 0
  a = len(list(data_dict.values()))
  for count in range(0, a - 6):
    sum = sum + list(data_dict.values())[count]["humidity"]
  result = sum / (a - 6)
  print(result)
  db.child("history").child(id).child(date).child(session).update(
    {"humidity": result})


#find  the average of body temperature
def body_temperature(db,id, date, session):
  data = db.child("history").child(id).child(date).child(session).get()
  data_dict = data.val()
  sum = 0
  a = len(list(data_dict.values()))
  for count in range(0, a - 7):
    sum = sum + list(data_dict.values())[count]["bdyTemp"]
  result = sum / (a - 7)
  print(result)
  db.child("history").child(id).child(date).child(session).update(
    {"body temp": result})

#function to retrive subpoints func 5
def retreiveonlysubsessions(db,table, id, date, session):
  summary = db.child(table).child(id).child(date).child(session).get()
  result_dict = {}

  for item in summary.each():

    if item.key() == "alt":
      break
    result_dict[item.key()] = item.val()
  keys = result_dict.keys()
  print(keys)

  #print(result_dict)

  return result_dict

#function to retrieve only summary func 6
def retrieve_only_summary(db,table, id, date, session):
  summary = db.child(table).child(id).child(date).child(session).get()
  result_dict = {}

  found_alt = False   

  for item in summary.each():
      if found_alt:
          if item.key() == "stp":
              break
          result_dict[item.key()] = item.val()
          
      elif item.key() == "alt":
          result_dict[item.key()] = item.val()
          found_alt = True
  print(result_dict)
  return result_dict

 # Update user data in Firebase
def update_user_data(db,request,id):
  table = 'users'  # Firebase table name
  #id = '715843108'  # User ID from the form or authentication system

  # Get the field values from the form
  name = request.values.get('name')
  email = request.values.get('email')
  phonenum = request.values.get('phonenum')
  dob=request.values.get('DOB')
  timeinterval=request.values.get('timeinterval')

  # Update user data in Firebase
  if name:
      db.child(table).child(id).update({'name': name})
  if email:
      db.child(table).child(id).update({'email': email})
  if phonenum:
      db.child(table).child(id).update({'phone': phonenum})
  if dob:
     db.child(table).child(id).update({'dob': dob})
  if timeinterval:
     db.child(table).child(id).update({'timeinterval': timeinterval})
  
     
  return 'User data updated successfully'

# Update user data in Firebase
def delete(db,request):
  table = 'history'  # Firebase table name
  id = '715843108'  # User ID from the form or authentication system

  # Get the field values from the form
  field= request.values.get('delete')
  

  # Update user data in Firebase
  db.child("history").child(id).child(field).remove()
  
     
  return 'deleted successfully'
 
#function for retrive previous summary
def get_pre_summary(db, id, date,session):
   
  date_node = db.child("history").child(id).child(date).get()
  session_keys = list(date_node.val().keys())
  current_index = session_keys.index(session)

  
  if current_index > 0:
    previous_session_key = session_keys[current_index - 1]
    # Access the previous session node
    previous_session_node = db.child("history").child(id).child(date).child(
      previous_session_key).get()

    # Get the dictionary representation of the previous session node
    previous_session_data = previous_session_node.val()

     
    if "alt" in previous_session_data:
      
      
      alt_index = list(previous_session_data.keys()).index("alt")
      
      data_after_alt = {
        k: v
        for k, v in list(previous_session_data.items())[alt_index:]
        if k not in ["strt", "stp", "strAd", "endAd"]
      }
       
      return data_after_alt
    else:
 
      return None
  else:
     
    return None  

def summarizer(db,userid,day_id,ses_id):
   #hrtRate=heart_rate(db,userid,day_id,ses_id)
   #bdyTemp=body_temperature(db,userid,day_id,ses_id)
   #envTemp=Etemp(db,userid,day_id,ses_id)
   #spd=speed(db,userid,day_id,ses_id)
   #hum=humidity(db,userid,day_id,ses_id)
   #alt=alt(db,userid,day_id,ses_id)
   return 0



