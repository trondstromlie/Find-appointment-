
import datetime
import time
import json
import sys
import types
import platform



class find_appointment:

    def __init__(self):

        #open the json file containing the "calender"
        #since we connect to this class on two diferent systems we check for os system
        if platform.system() == "Linux":
            with open("/storage/emulated/0/qpython/projects3/lege/calender.json") as calender:
              self.data = json.load(calender)
        elif platform.system() == "Windows" :
            with open("calender.json") as calender:
              self.data = json.load(calender)
        else:
            exit()


        self.summary_object = {"id":None,"doctor":None,"day":None,"type":None, "message":None,"time":[],"booking_ref":None}
        #index of selectetd doctor
        self.index = 0
        self.doc = []

#the "sett sumary object function"
    def set_value(self,value,type):
        if type == "doctor":

          if value in self.doc:
             self.summary_object["doctor"] = value
             self.summary_object["id"] = "id"
             return self.summary_object
          else:
             return "error"

        elif type == "time":
             self.summary_object["time"] = value
             return self.summary_object

        elif type == "type":
             self.summary_object["type"] = value
             return self.summary_object

        elif type == "day":
             self.summary_object["day"] = value
             return self.summary_object

        elif type == "message":
             self.summary_object["message"] = value
             return self.summary_object
        else:
            return self.summary_object


    #show list of available doctors
    def find_doctor(self):

        for doctor in range(len(self.data["doctor"])):
            menu_index = doctor + 1
            self.doc.append(self.data["doctor"][doctor]["name"])
        return self.doc




    #show list of available days for spesific doctor
    def available_day(self,index):
        #print("\nhvilken dag vil du ha legetime?\n{} har ledige timer følgende dager : ".format(self.summary_object["doctor"]))
        selected_day = []
        i = 0
        for x in self.data["doctor"][index]["calender"]:
            selected_day.append(x)
            i = i+1
        return selected_day




#show list of available appointment types
# type 15,30,45

    def appointment_type(self,index):

        appointent_types = []

        for i in range(len(self.data["doctor"][index]["slotts"])):
             appointent_types.append(self.data["doctor"][index]["slotts"][i])

        return appointent_types




#search the system for x numbers of slots in a row. return all possible appointments
    def open_slotts(self,index):

        #find all open slotts in the calender
        #number of slotts needed is type divided by 15 minutes

        slotts = int(self.summary_object["type"] /15)

        slotts_array = []
        good_slotts=[]
        populate_slots=[]

        #Iterate over all open slotts, if slotts  > 1 check that the next two
        #slotts are empty

        #for easy acces to data for interation we create a  list from the dict object
        for i in self.data["doctor"][index]["calender"][self.summary_object["day"]]:
            slotts_array.append(i)

        #now we start going over each index in  the list,
        #and look for x = (slotts_array) numbers of open slotts (slots not marked with None) in a row

        for x in range(len(slotts_array)) :

            if self.data["doctor"][index]["calender"][self.summary_object["day"]][slotts_array[x]]["appoint"]:
                s = self.data["doctor"][index]["calender"][self.summary_object["day"]].get(slotts_array[x],"None")
                #print(s["appoint"])

                check = []
                check.clear() #clear check on each iteration so we dont corrupt the controll

                for z in range(slotts):
                       e = (x + z)

                       if e < len(slotts_array):

                           s = self.data["doctor"][index]["calender"][self.summary_object["day"]].get(slotts_array[e],"No")

                           if self.data["doctor"][index]["calender"][self.summary_object["day"]][slotts_array[e]]["appoint"] == "None":
                                check.append(slotts_array[e])
                           else:
                                check.append("no")

                # now we write the three possible slotts to a list and
                # test if they are open

                if not "no" in check and len(check) == slotts:
                    good_slotts.append(check)


        if len(good_slotts) < 1:
            return "no free slotts today"
        else:
            return good_slotts


    #function skriv en melding til legen
    def write_message(self):
        print("skriv en melding til legen for å booke timen\n")
        message = input("skriv meldingen her, timen bokes i neste steg >> ")
        self.summary_object["message"] = message


    def book_apointment(self,doctor_id):
        #confirm and book the appointment

            #write to file
        slotts = int(self.summary_object["type"] /15)
        for i in range(slotts):
            self.data["doctor"][doctor_id]["calender"][self.summary_object["day"]][self.summary_object["time"][i]]["appoint"] = True
            self.data["doctor"][doctor_id]["calender"][self.summary_object["day"]][self.summary_object["time"][i]]["details"] = self.summary_object["message"]
        #with open('calender.json', 'w', encoding='utf-8') as calender:
        #    json.dump(self.data, calender, ensure_ascii=False, indent=4)


        if platform.system() == "Linux":
            with open("/storage/emulated/0/qpython/projects3/lege/calender.json", "w", encoding="utf-8") as calender:
                json.dump(self.data, calender, ensure_ascii=False, indent=4)
                return "ok"
        elif platform.system() == "Windows" :
            with open("calender.json", "w", encoding="utf-8") as calender:
                json.dump(self.data, calender, ensure_ascii=False, indent=4)
                return "ok, time er booket"
