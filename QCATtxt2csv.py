import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from tqdm import tqdm
import os
import sys
import csv


if __name__ == "__main__":
    dirpaths = '.'
    for dirpath in dirpaths:
        filenames = os.listdir(dirpath)
        for filename in filenames:
            if not filename.endswith(".txt") or len(filename) != 22:
                continue

            data = {'NR5G_MAC_CDRX_Events_Info':list(),
                    'LTE_ML1_CDRX_Events_Info':list()}

            try:
                filepath = os.path.join(dirpath, filename)
                print(filename)
                f = open(filepath, encoding="utf-8")
                print(">>>>>")
                current_pkg = ''
                temp = {}
                for_record = []
                record = []
                count = 0
                status = 'config'

                for l in f:
                    if l[0] == '%':
                        continue

                    # new package

                    if l[33:36] == '0xB':
                        status = 'config'
                        # print("new package")
                        if current_pkg != '':
                            temp['Records'] = record
                            for_record = []
                            record = []
                            data[current_pkg].append(temp)
                            # print(temp)
                        temp = {}

                        if l[33:39] == '0xB890':    # NR5G MAC CDRX Events Info
                            current_pkg = 'NR5G_MAC_CDRX_Events_Info'
                            for_record = ['#', 'System_Time_SCS', 'System_Frame_Number', 'Slot_Number', 'Prev_State', 'Current_State',
                                        'Reason', 'Current_Ref_Count', 'On_Duration_Start_Frame_Number', 'On_Duration_Start_Slot',
                                        'Short_Cycle_Timer_Frame_Number', 'Short_Cycle_Timer_Frame_Slot', 'Last_Grant_Time_Frame_Number',
                                        'Last_Grant_Time_Frame_Slot', 'Active_Procedure']

                        elif l[33:39] == '0xB198':  # LTE ML1 CDRX Events Info
                            current_pkg = 'LTE_ML1_CDRX_Events_Info'
                            for_record = ['SFN', 'Sub-fn', 'CDRX_Event', 'Internal_Field_Mask']

                        # Add other packages here
                        
                        else:
                            continue

                        temp['Time'] = l[0:25]
                        temp['Package_Name'] = l[41:-1].replace(" ", "_")
                        continue
                    
                    if current_pkg == '':
                        continue

                    if l[:7] == 'Records':
                        status = 'record0'
                        continue

                    if status == 'config':
                        # print(l[:-1].split('=')[-1])
                        temp[l[:-1].split('=')[0].strip().replace(" ", "_")] = l[:-1].split('=')[-1].strip()
                    
                    elif status[:6] == 'record':
                        if l[3:10] == '-------':
                            count = int(temp['Num_Records'])
                            status = 'record1' if status[-1] == '0' else 'record0'
                            continue
                        if status[-1] == '0' and count > 0:
                            ddata = l[4:-1].replace(" ", "").split('|')
                            dataa = {}
                            for i in range(0, len(for_record)):
                                dataa[for_record[i]] = ddata[i]
                            # print(dataa)
                            record.append(dataa)
                            count = count-1
                        else:
                            continue


                # NR5G_MAC_CDRX_Events_Info
                print(data['NR5G_MAC_CDRX_Events_Info'][0])
                with open(os.path.join(dirpath, filename[:-4]+'_NR5G_MAC_CDRX_Events_Info'+'.csv'), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter='@')
                    writer.writerow(['Time', 'Package_Name', 'Subscription_ID', 'Misc_ID', 'Major.Minor', 'Log_Fields_Change_BMask', 'Sub_ID', 'DRX_Enable',
                                    'On_Duration_Timer_Fraction', 'On_Duration_Time', 'Inactivity_Timer', 'DL_HARQ_RTT_Timer', 'UL_HARQ_RTT_Timer',
                                    'DL_Retransmission_Timer', 'UL_Retransmission_Timer', 'Long_DRX_Cycle_Start_Offset', 'Long_DRX_Cycle', 'Short_DRX_Cycle_Enable',
                                    'Short_DRX_Cycle_Timer', 'Short_DRX_Cycle', 'DRX_Slot_Offset', '#', 'System_Time_SCS', 'System_Frame_Number', 'Slot_Number',
                                    'Prev_State', 'Current_State', 'Reason', 'Current_Ref_Count', 'On_Duration_Start_Frame_Number', 'On_Duration_Start_Slot',
                                    'Short_Cycle_Timer_Frame_Number', 'Short_Cycle_Timer_Frame_Slot', 'Last_Grant_Time_Frame_Number', 'Last_Grant_Time_Frame_Slot', 'Active_Procedure'])
                    for j in data['NR5G_MAC_CDRX_Events_Info']:
                        # print(j)
                        for k in j['Records']:
                            print(k['#'])
                            writer.writerow([j['Time'], j['Package_Name'], j['Subscription_ID'], j['Misc_ID'], j['Major.Minor'], j['Log_Fields_Change_BMask'], j['Sub_ID'], j['DRX_Enable'],
                                            j['On_Duration_Timer_Fraction'], j['On_Duration_Time'], j['Inactivity_Timer'], j['DL_HARQ_RTT_Timer'], j['UL_HARQ_RTT_Timer'],
                                            j['DL_Retransmission_Timer'], j['UL_Retransmission_Timer'], j['Long_DRX_Cycle_Start_Offset'], j['Long_DRX_Cycle'], j['Short_DRX_Cycle_Enable'],
                                            j['Short_DRX_Cycle_Timer'], j['Short_DRX_Cycle'], j['DRX_Slot_Offset'], k['#'], k['System_Time_SCS'], k['System_Frame_Number'], k['Slot_Number'],
                                            k['Prev_State'], k['Current_State'], k['Reason'], k['Current_Ref_Count'], k['On_Duration_Start_Frame_Number'], k['On_Duration_Start_Slot'],
                                            k['Short_Cycle_Timer_Frame_Number'], k['Short_Cycle_Timer_Frame_Slot'], k['Last_Grant_Time_Frame_Number'], k['Last_Grant_Time_Frame_Slot'], k['Active_Procedure']])
                csvfile.close()


                # LTE_ML1_CDRX_Events_Info
                print(data['LTE_ML1_CDRX_Events_Info'][0])
                with open(os.path.join(dirpath, filename[:-4]+'_LTE_ML1_CDRX_Events_Info'+'.csv'), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter='@')
                    writer.writerow(['Time', 'Package_Name', 'Subscription_ID', 'Version', 'SFN', 'Sub-fn', 'CDRX_Event', 'Internal_Field_Mask'])
                    for j in data['LTE_ML1_CDRX_Events_Info']:
                        for k in j['Records']:
                            writer.writerow([j['Time'], j['Package_Name'], j['Subscription_ID'], j['Version'], k['SFN'], k['Sub-fn'], k['CDRX_Event'], k['Internal_Field_Mask']])
                csvfile.close()

                # Add other packages here


            except:
                continue
                
            

            

