import pytest


#checkboxes

def test_checkbox_select(page):
    checkbox = page.locator("input[value='option1']")
    checkbox.check()
    assert checkbox.is_checked()


def test_checkbox_uncheck(page):
    checkbox = page.locator("input[value='option2']")
    checkbox.check()
    checkbox.uncheck()
    assert not checkbox.is_checked()


def test_multiple_checkboxes(page):
    checkboxes = page.locator("input[type='checkbox']")
    for cb in checkboxes.all():
        cb.check()
        assert cb.is_checked()


#radio buttons

def test_radio_button_select(page):
    page.locator("input[value='radio2']").click()
    assert page.locator("input[value='radio2']").is_checked()


def test_only_one_radio_selected(page):
    page.locator("input[value='radio1']").click()
    page.locator("input[value='radio2']").click()
    # radio1 should now be deselected
    assert not page.locator("input[value='radio1']").is_checked()
    assert page.locator("input[value='radio2']").is_checked()


#static dropdown

def test_dropdown_select_by_value(page):
    dropdown = page.locator("#dropdown-class-example")
    dropdown.select_option("option2")
    assert dropdown.input_value() == "option2"


def test_dropdown_select_by_label(page):
    dropdown = page.locator("#dropdown-class-example")
    dropdown.select_option(label="Option3")
    assert dropdown.input_value() == "option3"


#autocomplete

def test_autocomplete_suggestions_appear(page):
    page.locator("#autocomplete").fill("Ind")
    page.wait_for_selector(".ui-menu-item")
    suggestions = page.locator(".ui-menu-item")
    assert suggestions.count() > 0


def test_autocomplete_select_option(page):
    page.locator("#autocomplete").fill("Ind")
    page.wait_for_selector(".ui-menu-item")
    page.locator(".ui-menu-item").filter(has_text="India").click()
    assert page.locator("#autocomplete").input_value() == "India"


#alert handling

def test_alert_accept(page):
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#alertbtn").click()


def test_confirm_dismiss(page):
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.locator("#confirmbtn").click()


#table

def test_table_has_rows(page):
    rows = page.locator("#product tbody tr")
    assert rows.count() > 0


def test_table_column_headers(page):
    headers = page.locator("#product thead th")
    header_texts = [h.inner_text() for h in headers.all()]
    assert "Firstname" in header_texts
    assert "Lastname" in header_texts


@pytest.mark.parametrize("country", ["India", "United States", "United Kingdom"])
def test_autocomplete_parameterized(page, country):
    # clear and re-fill for each country
    input_box = page.locator("#autocomplete")
    input_box.fill(country[:3])
    page.wait_for_selector(".ui-menu-item")
    page.locator(".ui-menu-item").filter(has_text=country).click()
    assert page.locator("#autocomplete").input_value() == country