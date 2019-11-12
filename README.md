jex
===
**J**SON **Ex**tractor

Why
---
I was asked this question in an interview, and ran out of time before I could
write a decent solution.

What
----
`jex` is a command line tool that extracts values from JSON input.  It's like
a minimal version of `jq`.

```console
$ cat input.json
{
    "food": {
        "vegetable": [
            {"name": "squash", "tasty": false},
            {"name": "carrot", "tasty": true}
        ],
        "fruit": [
            {"name": "apple", "tasty": true}
        ]
    }
}

$ jex 'food.vegetable.1.tasty' <input.json
true

$ jex 'food.vegetable.0' <input.json
{
    "name": "squash",
    "tasty": false
}

$ jex 'food.*.*.name' <input.json
["squash", "carrot", "apple"]
```

How
---
`jex` requires Python 3.7.  The makefile just copies the source file renamed to
`./jex` and marks it executable.
