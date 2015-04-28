# Plugins

## Plugin types

There are three types of plugins:

- web search
- indexable scripts
- searchable scripts

## Web Search
Web search is located solely in the DB. Containing an icon, title and website to go to, which has the tag {query} injectable to hook into URL-based searches.

## Indexable scripts
Scripts that return JSON structured data, the same format as apps; icon, name, command. This will be indexed by the same, same as the installed apps.

The indexable scripts that are shipped with Ducked are in ducked/plugins/indexables/

## Searchable scripts
Scripts that can be searched through realtime. Setup in the DB similarly to Web Search.

The searchable scripts that are shipped with Ducked are in ducked/plugin/searchables/
