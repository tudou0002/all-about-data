# Order Book
- Import `Websocket` for long lived connection and shorter time delay
- Use [Gimini public websocket](https://docs.gemini.com/websocket-api/#market-data) to get orderbook's data
- The first data flow will contain all the data at that point, following data will make changes based on the first one.