#!/usr/bin/env python3
import argparse

pythagorean_table = {
  'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,
  'g': 7,'h': 8,'i': 9,'j': 1,'k': 2,'l': 3,
  'm': 4,'n': 5,'o': 6,'p': 7,'q': 8,'r': 9,
  's': 1,'t': 2,'u': 3,'v': 4,'w': 5,'x': 6,
  'y': 7,'z': 8
}

chaldean_table = {
  'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 8,
  'g': 3,'h': 5,'i': 1,'j': 1,'k': 2,'l': 3,
  'm': 4,'n': 5,'o': 7,'p': 8,'q': 1,'r': 2,
  's': 3,'t': 4,'u': 6,'v': 6,'w': 6,'x': 5,
  'y': 1,'z': 7
}

def evaluate_numerology(word, table):
  return sum(map(lambda c: table[c] if c in table else 0, word.lower()))

def reduce_number(n):
  digits = []
  while n > 0:
    digits.append(n % 10)
    n = n // 10
  reduced = sum(digits)
  if (reduced < 10):
    return reduced
  else:
    return reduce_number(reduced)

def print_numerology(word, table, label, show_reduced, show_unreduced):
  raw = evaluate_numerology(word, table)
  reduced = reduce_number(raw)
  if show_reduced == show_unreduced:
    print(label + f'{raw}/{reduced}')
  elif show_unreduced:
    print(label + str(raw))
  else:
    print(label + str(reduced))

def create_numerology_output(args, word):
  int_print_numerology = lambda table, label: print_numerology(
    word, table, label, args.reduced, args.unreduced
  )
  if args.pythagorean == args.chaldean:
    int_print_numerology(chaldean_table, f'{word}: Chaldean ')
    int_print_numerology(pythagorean_table, f'{word}: Pythagorean ')
  else:
    label = '' if args.simple else f'{word}: '
    table = pythagorean_table if args.pythagorean else chaldean_table
    int_print_numerology(table, label)

def numerology_by_word(args):
  for word in args.input:
    create_numerology_output(args, word)

def numerology_by_line(args):
  for f in args.input:
    for line in f.split("\n"):
      if len(line) > 0:
        create_numerology_output(args, line)

def numerology_by_file_line(args):
  for filename in args.input:
    with open(filename) as f:
      for line in f:
        if line.endswith("\n"):
          line = line[:-1]
        create_numerology_output(args, line)

def make_parser():
  parser = argparse.ArgumentParser(
    description='Evaluate the numerology of one or more words.'
  )
  parser.add_argument('input', nargs='+', help='the input to evaluate')
  system_group = parser.add_mutually_exclusive_group()
  system_group.add_argument('-p', '--pythagorean',
    dest='pythagorean', action='store_true',
    help='use pythagorean numerology only')
  system_group.add_argument('-c', '--chaldean',
    dest='chaldean', action='store_true',
    help='use chaldean numerology only')
  output_group = parser.add_mutually_exclusive_group()
  output_group.add_argument('-r', '--reduced',
    dest='reduced', action='store_true',
    help='display the reduced values only')
  output_group.add_argument('-u', '--unreduced',
    dest='unreduced', action='store_true',
    help='display the unreduced values only')
  parser.add_argument('-s', '--simple',
    dest='simple', action='store_true',
    help='print the least amount of information necessary')
  source_group = parser.add_mutually_exclusive_group()
  source_group.add_argument('-w', '--words',
    dest='source', action='store_const', const='w', default='w',
    help='treat input as a list of words, evaluate of each word separately')
  source_group.add_argument('-l', '--lines',
    dest='source', action='store_const', const='l',
    help='treat input as a list of lines, evaluate numerology by line')
  source_group.add_argument('-f', '--file',
    dest='source', action='store_const', const='f',
    help='treat input as a list of files, evaluate numerology by line')
  return parser

if __name__ == '__main__':
  args = make_parser().parse_args()
  {
    'w': numerology_by_word,
    'l': numerology_by_line,
    'f': numerology_by_file_line
  }[args.source](args)
