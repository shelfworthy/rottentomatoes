rottentomatoes.py
=================

Changelog
---------

### V1.0.1
 * 100% test coverage.
 * Removal of all `+=` operators -- now using `''.join()` instead.

### V1.0
 * Initial release.


What is this?
------------

`rottentomatoes` offers an easy-to-use Python wrapper to interact with the
[Rotten Tomatoes API](http://developer.rottentomatoes.com/). Before you try and
use the API, make sure you sign up to get an API Key.

In order to cut down on boilerplate code, you can then save your API key in the
`rottentomatoes_api_key.py` file.

Also, note that this package is in no way associated or endorsed by
[RottenTomatoes.com](http://www.rottentomatoes.com/) or [Flixster,
Inc](http://www.flixster.com/).


Installation
------------

If you have `pip` installed, then run the following command:

    pip install rottentomatoes

You can also run `easy_install`:

    easy_install rottentomatoes

Or, if you want to help develop the package, just `git clone` the Github
repository:

    git clone https://github.com/zachwill/rottentomatoes.git


Usage
-----

* `search`  -- Rotten Tomatoes movie search. Returns:

- `pages`: how many pages of results there are. Get the next page by passing in a `page=2` argument.
- `movies`: a list of dictionarys describing each result movie.

``` python

>>> from rottentomatoes import RottenTomatoesClient
>>> rt = RottenTomatoesClient('my_api_key')
>>> rt.search('some movie here')

{'pages': 2,
 'movies': [<list of movies>]
}

```

* `lists` -- Rotten Tomatoes Lists.

Calling this funcion witout any args will return the top level list of lists:

``` python

rt.lists()

{u'dvds': <rottentomatoes.rottentomatoes.List at 0x1032de090>,
 u'movies': <rottentomatoes.rottentomatoes.List at 0x1032de890>}

```

lists current have a single `.get()` method that is used to get their contents (either more lists of movies):

``` python

rt.lists()['dvds'].get()

{u'current_releases': <rottentomatoes.rottentomatoes.List at 0x1032de610>,
 u'new_releases': <rottentomatoes.rottentomatoes.List at 0x1032de0d0>,
 u'top_rentals': <rottentomatoes.rottentomatoes.List at 0x1032de8d0>,
 u'upcoming': <rottentomatoes.rottentomatoes.List at 0x1032de190>}

 ```
it is also possible to send the `directory` arg to lists to get a list directly:

``` python

rt.lists('dvds/current_releases')

{'pages': 1,
 'movies': [<list of movies>]
}

```

License
-------

**Author**: Zach Williams, Chris Drackett
