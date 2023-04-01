# BlockKitAPI
* As by-product of my project at University of Glasgow, I have developed a Block Kit API for working with Slack's blocks and surfaces. The motivation stemmed from the frustration when dealing with Python dictionaries rather than specific classes. 

* For example, instead of manually defining this:
```
{
	"type": "home",
	"blocks": [
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click Me",
						"emoji": true
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		}
	]
}
```
We can use the API to do it more programatically:
```
home_surface = HomeSurface()

button = Button(
    text=Text(type="plain_text", text="Click Me"),
    action_id="click_me_123",
    value="actionId-0"
)

action_block = ActionBlock(elements=[button])

home_surface.add(action_block)
```
Moreover, if we feel like changing the payload value for button, all we have to do is:
```
button.value = "foo"
```
instead of navigating over dictionary.
Lastly, this API offers error checking hence, the UI of your applications can be properly and easily tested. 

* **This API is still under development but feel free to use it.**
* **Under Apache license v2.0**
