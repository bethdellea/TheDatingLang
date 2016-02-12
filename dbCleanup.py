''' Feb 8, 2016 ---- we need to get rid of the profiles in our database
which are empty or encoded wrong and totally useless to us. It'll make life a
lot easier for us down the line.
- Beth (hello yes that was a weirdly long opening comment. ANYway.)
'''

#borrowed from a sqlfiddle linked to by a stack overflow post
    #this is the basic process we'll need to do
#but we'll look cooler doing it


CREATE TABLE test (
  _id INTEGER PRIMARY KEY AUTOINCREMENT,
  value VARCHAR(32)
);

INSERT INTO test (value) VALUES ('Value#1');
INSERT INTO test (value) VALUES ('Value#2');
INSERT INTO test (value) VALUES ('Value#3');

DELETE FROM test WHERE _id=2;

CREATE TABLE test2 AS SELECT * FROM test;
DELETE FROM test;
DELETE FROM sqlite_sequence WHERE name='test';
INSERT INTO test (value) SELECT value FROM test2;
DROP TABLE test2;
