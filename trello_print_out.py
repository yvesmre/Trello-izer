import tkinter
from functools import partial
from trello_imports import *
import os, subprocess, platform
from openpyxl import load_workbook
from openpyxl.styles import Font

def fit_text_to_widget(text_widget):
    # Get the number of lines and the longest line's length
    num_lines = int(text_widget.index('end-1c').split('.')[0])
    longest_line_length = max(len(line) for line in text_widget.get("1.0", "end-1c").split('\n'))

    # Calculate the widget's required height and width
    height = int(int(longest_line_length/(512/8))*2)
    width = int(min(longest_line_length, 512/8))

    # Resize the widget to fit the text
    text_widget.config(width=width, height=height)

def all_children (wid) :
    _list = wid.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list




def create_spreadsheet(board_id, job_no, filename):

    #Hacky way of going about this, tbh
    if not os.path.exists(os.getcwd() + "/" + filename.split('/')[1]) :
        os.makedirs(os.getcwd() + "/" + filename.split('/')[1])

    board = import_cards_with_custom_fields_from_board(board_id)

    to_json = {"Checklist": [], 
                'Part No.': [], 
            #    "Member": [], "Completion": [], 
            #    "Card Last Modified": []
                    }

    user_to_name = {}
    for card in board:
        checklists = import_checklist(card['id'])

        card_name = card['name']
        if not (card_name.split('-')[0].replace('#', '').strip() == job_no): continue

        for obj in checklists:

            part_found = []
            for checklist_item in obj["checkItems"]:
                if("Part No." in checklist_item['name']):
                    to_json['Checklist'].append(obj['name'])
                    to_json['Part No.'].append(checklist_item['name'].replace("Part No.", ''))
                    part_found.append(checklist_item['name'].replace("Part No.", ''))
            if not part_found: 
                to_json['Checklist'].append(obj['name'])
                to_json['Part No.'].append('N/A' if not part_found else ''.join([f'[{s}], ' if i < len(part_found) - 1 else f'[{s}]' for i, s in enumerate(part_found)]))

        break

    frame = pd.DataFrame(data=to_json)

    # frame.drop_duplicates()
    writer = StyleFrame.ExcelWriter(os.getcwd() + filename)
    sf = StyleFrame(frame)


    #   sf.set_column_width(columns='Card Title', width=25)
    sf.set_column_width(columns='Checklist', width=70)
    sf.set_column_width(columns='Part No.', width=50)
    #   sf.set_column_width(columns='Member', width=25)
    #   sf.set_column_width(columns='Card Last Modified', width=20)
    #   sf.set_column_width(columns='Completion', width=20)
    sf.to_excel(excel_writer=writer, row_to_add_filters=2,index=False)

    writer.close()

    wb = load_workbook(os.getcwd()+ filename)
    ws = wb.active

    # Insert blank rows at the top
    ws.insert_rows(1, 2)

    ws.cell(row=1, column=1, value="Build Out Sheet").font = Font(size = 27, bold=True)
    ws.cell(row=2, column=1, value="JOB CARD: " + card_name).font = Font(size = 24, bold=True, underline='single')
    
    merge_start = 1

    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=1).value != ws.cell(row=row-1, column=1).value:
            if merge_start < row - 1:
                ws.merge_cells(start_row=merge_start, start_column=1, end_row=row-1, end_column=1)
            merge_start = row

    # Handle the last merge range in the first column
    if merge_start < ws.max_row:
        ws.merge_cells(start_row=merge_start, start_column=1, end_row=ws.max_row, end_column=1)

    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=1):
        for cell in row:
            if cell.value:
                lines = int(len(str(cell.value)) / 70)
                ws.row_dimensions[cell.row].height = (lines * 30) 

    wb.save(os.getcwd()+ filename)

    #Linux compatibility begone!
    subprocess.call(['open', os.getcwd()+ filename]) if platform.system() == "Darwin" else os.startfile(os.getcwd()+ filename)


if __name__ == "__main__":
    def search_card(widget):
        # board = import_cards_with_custom_fields_from_board(FIT_OUT_BOARD if not USE_TESTING_LIST else TEST_LIST)

        label = tkinter.Label(m, text="Searching...")
        label.grid(row=4, column=1)
        label.config(bg="green")

        thread = Thread(target=create_spreadsheet, args=(FIT_OUT_BOARD, widget.get(), "/output/" + widget.get() + ".xlsx"))
        thread.start()
   
        # label.destroy()
        # for child in all_children(m):
        #     if type(child) == tkinter.Text:
        #         child.destroy()

        # for card in board:
        #     card_id = card['id']
        #     job_no = card["name"].split('-')[0].replace('#','').strip()

        #     if (job_no==widget.get()):
                
        #         checklists = import_checklist(card_id)

        #         name = tkinter.Text(m)
        #         name.insert("1.0", card["name"])
        #         name.grid(row=3, column=1)
        #         fit_text_to_widget(name)

        #         for obj in checklists:
        #             text = tkinter.Text(m, wrap="word")
        #             text.insert('1.0', obj['name'].strip())
        #             text.grid(row=4+checklists.index(obj), column=1)
        #             fit_text_to_widget(text)
                 
    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)

    tkinter.Label(m, text='Job No.').grid(row=0, column=1)

    e1 = tkinter.Entry(m)
    e1.grid(row=1, column=1)

    start_button = tkinter.Button(m, text="Get Card Details", command=partial(search_card, e1))
    start_button.grid(row=2, column=1)

    m.mainloop()

