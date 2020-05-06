from model import find_appointment
import androidhelper as android
import datetime
import time
import json
import sys
import types

droid = android.Android()

class new_appontment:

        def __init__(self):

            self.new = find_appointment()
            self.index = None


            title = 'Program starter'
            message = 'Søker etter tilgjengelig lege.'
            droid.dialogCreateSpinnerProgress(title, message)
            droid.dialogShow()
            time.sleep(1)


            self.velgLege()
            self.velgDag()
            self.velgType()
            self.velgTime()
            self.meldingTilLege()
            self.conformAppointment()

            droid.dialogDismiss()

        #velg legen
        #fetch list ov available doctors
        def velgLege(self):
            doc = self.new.find_doctor()
            title = 'Velg lege'
            droid.dialogCreateAlert(title)
            droid.dialogSetItems(doc)
            droid.dialogShow()
            response = droid.dialogGetResponse().result
            self.index=response["item"]

            #send back selected doctor, write value to summary_object set_value(doctor_name,doctor ID, type of request)
            selectet_doctor = self.new.set_value(doc[response["item"]],"doctor")


        #velg dag
        #fetch list of available days
        def velgDag(self):
            day = self.new.available_day(self.index)
            select_doc = None
            doctor_id = None
            title = 'Velg Dag'
            droid.dialogCreateAlert(title)
            droid.dialogSetItems(day)
            droid.dialogShow()
            response = droid.dialogGetResponse().result

            #send back selected day, write value to summary_object
            selectet_day = self.new.set_value(day[response["item"]],"day")

        #velg timetype
        def velgType(self):
            type = self.new.appointment_type(self.index)
            select_doc = None
            doctor_id = None
            title = 'Velg timetype'
            droid.dialogCreateAlert(title)
            droid.dialogSetItems(type)
            droid.dialogShow()
            response = droid.dialogGetResponse().result

            #send back selected appointment type, write value to summary_object
            selectet_type = self.new.set_value(type[response["item"]],"type")


        #velg timen
        #fetch list of available slotts fiting your appointment type
        def velgTime(self):
            time_slotts = self.new.open_slotts(self.index)
            time = []

            for i in range(len(time_slotts)):
                time.append(time_slotts[i][0])

            select_doc = None
            doctor_id = None
            title = 'Velg din time'
            droid.dialogCreateAlert(title)
            droid.dialogSetItems(time)
            droid.dialogShow()
            response = droid.dialogGetResponse().result

            #send back selected doctor, write value to summary_object
            selectet_time = self.new.set_value(time_slotts[response["item"]],"time")


        def meldingTilLege(self):
            droid.dialogCreateInput(title="Skriv melding til lege",message="vendligst skriv en melding her:",defaultText=None,inputType=None)
            droid.dialogSetPositiveButtonText('legg ved melding!')
            droid.dialogShow()
            response = droid.dialogGetResponse().result
            print(response["value"])
            message = self.new.set_value(response["value"],"message")

        def conformAppointment(self):
            #bekreft din timebestilling
            value = self.new.set_value(0 ,0)



            title = 'bekreft din bestilling'
            mes = ""
            for k,v in value.items():
                #print(str(k)+str(v))
                mes += "\n {} {}\n".format(str(k),str(v))

            droid.dialogCreateAlert(title, mes)
            droid.dialogSetPositiveButtonText('Yes')
            droid.dialogSetNegativeButtonText('No')
            droid.dialogShow()
            response = droid.dialogGetResponse().result


            if response['which'] == 'positive':
                book = self.new.book_apointment(self.index)
                title = 'booker din time'
                message = 'dette kan ta noen få sekunder.'
                droid.dialogCreateHorizontalProgress(title, message, 50)
                droid.dialogShow()
                for x in range(0, 50):
                     time.sleep(0.1)
                     droid.dialogSetCurrentProgress(x)
                #droid.dialogDismiss()
                if book == "ok":

                    droid.vibrate()
                    title = 'Du er registrert'
                    message = ('Din time er registrert, møt opp i god tid.')
                    droid.dialogCreateAlert(title, message)
                    droid.dialogSetPositiveButtonText('ok')
                    droid.dialogShow()
                    response = droid.dialogGetResponse().result

                else:
                    exit()



            else:
                exit()




if __name__ == "__main__":

    x = new_appontment()
