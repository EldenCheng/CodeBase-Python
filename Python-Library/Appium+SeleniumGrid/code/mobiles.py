from appium.options.android import UiAutomator2Options


capabilities_s9plus = dict(
    platformName='Android',
    deviceName='Galaxy S9+'
)
capabilities_note10 = dict(
    platformName='Android',
    deviceName='Galaxy Note10',
)
capabilities_note9 = dict(
    platformName='Android',
    deviceName='Galaxy Note9',
)
capabilities_note20 = dict(
    platformName='Android',
    deviceName='Galaxy Note20',
)
capabilities_s10 = dict(
    platformName='Android',
    deviceName='Galaxy S10'
)
capabilities_s20fe = dict(
    platformName='Android',
    deviceName='Galaxy S20FE'
)
capabilities_s205g = dict(
    platformName='Android',
    deviceName='Galaxy S205G'
)
capabilities_s22 = dict(
    platformName='Android',
    deviceName='Galaxy S22'
)
capabilities_pixel7pro = dict(
    platformName='Android',
    deviceName="Pixel 7Pro"
)
capabilities_pixel2xl = dict(
    platformName='Android',
    deviceName="Pixel 2XL"
)
capabilities_tabs2 = dict(
    platformName='Android',
    deviceName="Galaxy Tab S2"
)
capabilities_tabs7plus = dict(
    platformName='Android',
    deviceName="Galaxy Tab S7Plus"
)

options_s9plus = UiAutomator2Options().load_capabilities(capabilities_s9plus)
options_s10 = UiAutomator2Options().load_capabilities(capabilities_s10)
options_s20fe = UiAutomator2Options().load_capabilities(capabilities_s20fe)
options_s205g = UiAutomator2Options().load_capabilities(capabilities_s205g)
options_s22 = UiAutomator2Options().load_capabilities(capabilities_s22)
options_note10 = UiAutomator2Options().load_capabilities(capabilities_note10)
options_note9 = UiAutomator2Options().load_capabilities(capabilities_note9)
options_note20 = UiAutomator2Options().load_capabilities(capabilities_note20)
options_pixel7pro = UiAutomator2Options().load_capabilities(capabilities_pixel7pro)
options_pixel2xl = UiAutomator2Options().load_capabilities(capabilities_pixel2xl)
options_tabs2 = UiAutomator2Options().load_capabilities(capabilities_tabs2)
options_tabs7plus = UiAutomator2Options().load_capabilities(capabilities_tabs7plus)