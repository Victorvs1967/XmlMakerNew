import PySimpleGUI as sg

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import sys


publication_plan = {'publication_plan':
                        {'unit': 'mm',
                        'publication': 'ВЕСТИ',
                        'edition': 'VST',
                        'pubdate': '010118',
                        'pages': '105'}}

page = {'physical_page_number': '1',
        'logical_page_number': '1',
        'base_editions': "BUF",
        'height': '375',
        'width': '259',
        'colour': '4',
        'unique_id': 'ВЕСТИ_BUF_',
        'modifier': '00',
        'section': 'BUF',
        'dps': '0'}

base_editions_array = ['BUF', 'SEC', 'DNE', 'ODS', 'KHA', 'UKR', 'KIE']
sections12 = ['BUF', 'FST', 'STR', 'STR', 'STR', 'STR', 'GRD', 'GRD', 'MIR', 'POK', 'CUL', 'SRT', 'LST', 'AVT', 'DSG',
            'FIN', 'NDV', 'OBU', 'RBT', 'SEM', 'SIT', 'TCH', 'TOP', 'ZDR', 'DON', 'DNE']
sections16 = ['BUF', 'FST', 'STR', 'STR', 'STR', 'STR', 'GRD', 'GRD', 'MIR', 'POK', 'CUL', 'SRT', 'AVT', 'DSG', 'FIN',
            'NDV', 'LST', 'OBU', 'RBT', 'SEM', 'SIT', 'TCH', 'TOP', 'ZDR', 'DON', 'DNE']

def xmlCreate(start_date):
    """"""
    date = start_date    
    day = int(date[0:2])
        
    for i in [1, 3, 4]:
        if day < 10:
            date = '0' + str(day) + date[2:]
        else:
            date = str(day) + date[2:]

        publication_plan['publication_plan']['pubdate'] = date

        if i == 1:
            day += 2
        else:
            day += 1
        
        for name in publication_plan.keys():
            pub = Element(name)
            for key, value in publication_plan['publication_plan'].items():
                pub_element = SubElement(pub, key)
                pub_element.text = value
        
        for edition in base_editions_array:
            if edition == 'BUF':
                sections = sections12
                k = 21
            elif edition == 'SEC':
                sections = sections12
                k = 26
            else:
                sections = sections16
                k = 17

            for i in range(1, k):
                page['physical_page_number'] = str(i)
                page['logical_page_number'] = str(i)
                page['base_editions'] = edition
                page['height'] = '375'
                page['width'] = '259'
                page['colour'] = '4'
                page['unique_id'] = 'ВЕСТИ_' + edition + '_' + date + '_' + str(i)
                page['modifier'] = 'OO'
                if edition == 'BUF':
                    page['section'] = edition
                else:
                    page['section'] = sections[i]
                page['dps'] = '0'

                page_xml = Element('page')
                for page_key, page_value in page.items():
                    page_element = SubElement(page_xml, page_key)
                    page_element.text = page_value
                pub.append(page_xml)

        xml = parseString(tostring(pub)).toprettyxml(' ')
        file_name = './VST_20' + date[4:] + '_' + date[2:4] + '_' + date[0:2] + '.xml'
        print(file_name)
        with open(file_name, 'w', encoding='utf-8') as fileOutput:
            fileOutput.write(xml)
    
def maker_gui():
    sg.theme('Dark Blue 13')
    layout = [
        # [sg.Text('Title 1'), sg.InputText(), sg.FileBrowse(), sg.Checkbox('Chk01'), sg.Checkbox('Chk02')],
        # [sg.Text('Title 2'), sg.InputText(), sg.FileBrowse(), sg.Checkbox('Chk03'), sg.Checkbox('Chk04')],
        # # [sg.Output(size=(100, 40))],
        [sg.Text('Start date (DDMMYY)', font=('Helvetica', 14)), sg.InputText(size=(10, 1), font=('Helvetica', 16))],
        [sg.Output(size=(80, 10))],
        [sg.Submit(size=(8, 1), font=('Helvetica', 16)), sg.Cancel(size=(8, 1), font=('Helvetica', 16))]
    ]
    window = sg.Window('Main Title', layout)
    
    while True:
        event, values = window.read()
        if event == 'Submit':
            xmlCreate(values[0])
            print('Xml ready...')
            
        if event in (None, 'Exit', 'Cancel'):
            break

if __name__ == '__main__':

    maker_gui()
