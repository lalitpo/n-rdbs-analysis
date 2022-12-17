## Mapping common SQL predicates to RediSearch

| SQL Condition                            | RediSearch Equivalent              | Comments                                 |
| -----------------------------------------|------------------------------------|------------------------------------------|
| WHERE x='foo' AND y='bar'                | @x:foo @y:bar                      | for less ambiguity use (@x:foo) (@y:bar) |
| WHERE x='foo' AND y!='bar'               | @x:foo -@y:bar                     |                                          |
| WHERE x='foo' OR y='bar'                 | (@x:foo)|(@y:bar)                  |                                          |
| WHERE x IN ('foo', 'bar','hello world')  | @x:(foo|bar|"hello world")         | quotes mean exact phrase                 |
| WHERE y='foo' AND x NOT IN ('foo','bar') | @y:foo (-@x:foo) (-@x:bar)         |                                          |
| WHERE x NOT IN ('foo','bar')             | -@x:(foo|bar)                      |                                          |
| WHERE num BETWEEN 10 AND 20              | @num:[10 20]                       |                                          |
| WHERE num >= 10                          | @num:[10 +inf]                     |                                          |
| WHERE num > 10                           | @num:[(10 +inf]                    |                                          |
| WHERE num < 10                           | @num:[-inf (10]                    |                                          |
| WHERE num <= 10                          | @num:[-inf 10]                     |                                          |
| WHERE num < 10 OR num > 20               | @num:[-inf (10] \| @num:[(20 +inf] |                                          |
| WHERE name LIKE 'john%'                  | @name:john*                        |                                          |
