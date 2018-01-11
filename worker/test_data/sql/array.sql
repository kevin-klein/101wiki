CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
);

INSERT INTO sal_emp
    VALUES ('Bill',
    '{10000, 10000, 10000, 10000}',
    '{{"meeting", "lunch"}, {"training", "presentation"}}');

SELECT name FROM sal_emp WHERE pay_by_quarter[1] <> pay_by_quarter[2];
UPDATE sal_emp SET pay_by_quarter = '{25000,25000,27000,27000}'
    WHERE name = 'Carol';

UPDATE sal_emp SET pay_by_quarter[1:2] = '{27000,27000}'
  WHERE name = 'Carol';


SELECT array_dims(1 || '[0:1]={2,3}'::int[]);
SELECT f1[1][-2][3] AS e1, f1[1][-1][5] AS e2
 FROM (SELECT '[1:1][-2:-1][3:5]={{{1,2,3},{4,5,6}}}'::int[] AS f1) AS ss;
