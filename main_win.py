#main.py

from model import find_appointment

def new_appontment():
    new = find_appointment()

    #velg lege
    print("\nVelg din lege")
    doc = new.find_doctor()
    for d in range(len(doc)):
        print("{} : {}".format(d+1,doc[d]))

    select_doc = input("velg din lege fra menyen, nummer 1 til {} >> ".format(len(doc)))
    doctor_id = int(select_doc)-1
    selectet_doctor = new.set_value(doc[doctor_id],"doctor")

    #velg dag
    days = new.available_day(doctor_id)
    print("\n {} jobber følgende dager: \n".format(doc[doctor_id]))
    for d in range(len(days)):
        print("{} : {}".format(d+1,days[d]))

    select_day = input("velg din dag fra menyen, nummer 1 til {} >> ".format(len(days)))
    day_i = int(select_day)-1
    selected_day = new.set_value(days[day_i],"day")

    #velg timetype
    appointment_types = new.appointment_type(doctor_id)
    print("\n {} har disse timetypene: \n".format(doc[doctor_id]))
    for d in range(len(appointment_types)):
        print("{} : {}".format(d+1,appointment_types[d]))

    select_type_i = input("velg din timetype fra menyen, nummer 1 til {} >> ".format(len(appointment_types)))
    type_i = int(select_type_i)-1
    selected_type = new.set_value(appointment_types[type_i],"type")
    #print(selected_type)

    #velg timen
    print(doctor_id)
    appointment_times = new.open_slotts(doctor_id)
    print("\n {} har disse ledige timene: \n".format(doc[doctor_id]))
    for d in range(len(appointment_times)):
        print("{} : {}".format(d+1,appointment_times[d]))
    select_time_i = input("velg din timetype fra menyen, nummer 1 til {} >> ".format(len(appointment_times)))
    time_i = int(select_time_i)-1
    selected_time = new.set_value(appointment_times[time_i],"time")
    #print(selected_time)


    #skriv melding til legen
    print("skriv en melding til legen\n du bekrefter timen i neste steg")
    message_i = input("Skriv melding til legen her >>")
    message = new.set_value(message_i ,"message")
    #print(message)


    #bekreft din timebestilling
    print(new.set_value(0 ,0))
    print("vil du booke denne avtalen")
    conf_in = input("y = yes n = no >> ")
    if conf_in == "y":
        confirm = new.book_apointment(doctor_id)
        print(confirm)


    #new_appointment.available_day()
    #new_appointment.show_appointment_type()
    #new_appointment.open_slotts()
    #new_appointment.write_message()
    #new_appointment.book_apoinment()

if __name__ == "__main__":

    new_appontment()
