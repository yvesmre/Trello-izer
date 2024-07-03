import requests
import json
import pandas as pd
from variables import *
import tkinter
from threading import *

headers = {
  "Accept": "application/json"
}

def get_cards(board):

  board_url = "https://api.trello.com/1/boards/" + board + "/cards"

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
    "customFieldItems":"true"
  }

  response = requests.request(
    "GET",
    board_url,
    headers=headers,
    params=query
  )


  JSON_response = json.loads(response.text)

  return json.dumps(JSON_response, sort_keys=True, indent=4, separators=(",", ": "))

  


def look_for_duplicates(board, name):
    
  url = "https://api.trello.com/1/boards/" + board + "/cards"

  query = {
  'key': API_KEY,
  'token': AUTH_TOKEN
  }

  response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
  ) 

  JSON_response = json.loads(response.text)

  seen = []
  duplicates = []
  for obj in JSON_response:
      job_no = obj["name"].split('-')[0].replace("#", " ")
      if not (any(c.isalpha() for c in job_no)):
          if job_no.strip() not in seen:
              seen.append(job_no.strip())
          else: duplicates.append(job_no.strip())


  return duplicates

def all_children (wid) :
    _list = wid.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def fit_text_to_widget(text_widget):
    # Get the number of lines and the longest line's length
    num_lines = int(text_widget.index('end-1c').split('.')[0])
    longest_line_length = max(len(line) for line in text_widget.get("1.0", "end-1c").split('\n'))

    # Calculate the widget's required height and width
    height = int(int(longest_line_length/(512/8))*2.5)
    width = int(min(longest_line_length, 512/8))

    # Resize the widget to fit the text
    text_widget.config(width=width, height=height)

if __name__ == "__main__":
    

    def run_task():
      children = all_children(m)

      for child in children:
          if type(child) == tkinter.Text:
              child.destroy()
          if(type(child) ==tkinter.Label):
                  child.destroy()

      drafting_dupes = look_for_duplicates(DRAFTING_BOARD, "Drafting")
      fit_out_dupes = look_for_duplicates(FIT_OUT_BOARD, "Fit Out")

      draft_header = tkinter.Text(m, wrap="word")
      draft_header.insert('1.0', "Drafting Duplicates")
      draft_header.grid(row=2, column = 0)
      fit_text_to_widget(draft_header)
      for i in range(len(drafting_dupes)):
        text_entry = tkinter.Text(m, wrap="word")
        text_entry.insert('1.0', drafting_dupes[i])
        text_entry.config(bg='gray30', fg="white")
        text_entry.grid(row=i+3, column=0)
        text_entry.config(state="disabled")
        fit_text_to_widget(text_entry)

      fit_out_header = tkinter.Text(m, wrap="word")
      fit_out_header.insert('1.0', "Fit Out Duplicates")
      fit_out_header.grid(row=2, column = 2)
      fit_text_to_widget(fit_out_header)
      for i in range(len(fit_out_dupes)):
        text_entry = tkinter.Text(m, wrap="word")
        text_entry.insert('1.0', fit_out_dupes[i])
        text_entry.config(bg='gray30', fg="white")
        text_entry.grid(row=i+3, column=2)
        text_entry.config(state="disabled")
        fit_text_to_widget(text_entry)

    def button():
      Thread(target=run_task).start()
                 
    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)


    start_button = tkinter.Button(m, text="Look for Duplicates", command=button, height=4, width=16)
    start_button.grid(row=1, column=1)

    m.mainloop()


