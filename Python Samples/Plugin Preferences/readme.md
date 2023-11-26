## Add plugin settings to the App’s settings window

Make an object that behaves like a NSViewController (either by using on, or base your plugin on it). then add this:
(python)
```
	def loadPlugin(self):
		self.view() # sure to load the view
		appDelegate = NSApp.delegate()
		try:
			appDelegate.addViewToPreferences_(self)
		except:
			print("Could not add preference")
```
(Objective-C)
```
- (void)loadPlugin {
	[self view]; // sure to load the view
	NSObject<GSAppDelegateProtocol> *appDelegate = (NSObject<GSAppDelegateProtocol> *)[NSApp delegate];
	if ([appDelegate respondsToSelector:@selector(addViewToPreferences:)]) {
		[appDelegate addViewToPreferences:self];
	}
	else {
		NSLog(@"Could not add preference");
	}
}
```