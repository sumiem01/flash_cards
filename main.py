import database
import os.path

PROMPT = "> "

def print_help():
  help = '''
         What you want to do?
         To see help again: help
         To add a question: add polish_word english_translation
         To show your questions: show
         To delete a question: delete id
         To update a question: update polish_word english_translation id
         To play: play
         To clear screen: clear
         To quit: quit\n'''

  print(help)
  

def parse_commands(conn):
  '''Parse user commands. Return False if user wants to quit the app.'''

  command = input(PROMPT)

  words = command.split()
  if words[0] == 'help':
    print_help()
  elif words[0] == 'add':
    question = (words[1], words[2])
    database.add_question(conn, question)
    database.show_questions(conn)
  elif words[0] == 'show':
    database.show_questions(conn)
  elif words[0] == 'delete':
    database.delete_question(conn, int(words[1]))
    database.show_questions(conn)
  elif words[0] == 'update':
    question = (words[1], words[2], words[3])
    database.update_question(conn, question)
    database.show_questions(conn)
  elif words[0] == 'quit':
    return False
  elif words[0] == 'play':
    play(conn)
    print_help()
  elif words[0] == 'clear':
    for i in range(100):
      print('\n')

  return True

def get_database_questions_count(conn):
  sql = 'SELECT Count(*) FROM questions'
  cur = conn.cursor()
  cur.execute(sql)
  count = cur.fetchall()[0][0]

  return count


def play(conn):
  ''' Play the flash cards game until user inputs "quit" '''

  if get_database_questions_count(conn) < 1:
    print("Cannot play! No questions in database!")
    return

  print("I will give you a polish word, you must provide an english translation. To exit write: quit. Let's go!\n")
  sql = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1'
  cur = conn.cursor()
  good_answers = 0
  asked_questions = 0

  while True:
    cur.execute(sql)
    row = cur.fetchall()[0]
    question = row[1]
    answer = row[2]

    while True:
      i = input("Translate: " + question + "\n" + PROMPT)
      if i == answer:
        good_answers += 1
        asked_questions += 1
        break
      elif i == 'IamStupid':
        print("The answer is: " + answer )
      elif i == 'quit':
        print("Game over :) You asked properly " + str(good_answers) + " out of " + str(asked_questions) + " questions.")
        return
      else:
        print("Nope :( Try again. Write: IamStupid - to check the answer, quit - to quit.")
        asked_questions += 1


def main():

  dbfile = r"flash_cards.db"

  if not os.path.isfile(dbfile):
    print("Database not found in current directory! Creating a new one.")
    database.create_new_questions_database(dbfile)

  conn = database.create_connection(dbfile)
  with conn:
    print_help()

    while parse_commands(conn):
      pass


if __name__ == '__main__':
    main()
