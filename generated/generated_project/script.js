// Calculator implementation for the web calculator UI
// ---------------------------------------------------
// The Calculator class manages the state of the calculator and provides
// methods that correspond to the UI actions (digit entry, decimal point,
// sign toggle, clear, operator selection, equals, and percentage).

class Calculator {
  /**
   * @param {HTMLElement} displayElement - The element where the current value is shown.
   */
  constructor(displayElement) {
    this.displayElement = displayElement;
    // The value currently being typed/displayed (as a string to preserve formatting).
    this.currentInput = "0";
    // The stored value from a previous operation (as a number).
    this.previousValue = null;
    // The pending operator ("+", "-", "*", "/").
    this.operator = null;
    this.updateDisplay();
  }

  /** Update the calculator's visual display. */
  updateDisplay() {
    // Remove leading zeros except when the value is exactly "0" or starts with "0.".
    let display = this.currentInput;
    if (!display.includes(".")) {
      // Trim leading zeros for integer part.
      display = parseInt(display, 10).toString();
    }
    this.displayElement.textContent = display;
  }

  /** Append a digit to the current input. */
  inputDigit(digit) {
    if (this.currentInput === "0") {
      // Replace leading zero unless we are entering a decimal number like "0.".
      this.currentInput = digit;
    } else {
      this.currentInput += digit;
    }
    this.updateDisplay();
  }

  /** Insert a decimal point if one does not already exist. */
  inputDecimal() {
    if (!this.currentInput.includes(".")) {
      this.currentInput += ".";
      this.updateDisplay();
    }
  }

  /** Toggle the sign of the current input. */
  toggleSign() {
    if (this.currentInput.startsWith("-")) {
      this.currentInput = this.currentInput.substring(1);
    } else if (this.currentInput !== "0") {
      this.currentInput = "-" + this.currentInput;
    }
    this.updateDisplay();
  }

  /** Clear the current entry (CE). */
  clearEntry() {
    this.currentInput = "0";
    this.updateDisplay();
  }

  /** Reset the entire calculator (AC). */
  allClear() {
    this.currentInput = "0";
    this.previousValue = null;
    this.operator = null;
    this.updateDisplay();
  }

  /** Store the selected operator and prepare for the next operand. */
  setOperator(op) {
    // If there is already a pending operation, compute it first.
    if (this.operator && this.previousValue !== null) {
      this.calculateResult();
    }
    this.operator = op;
    // Save the current input as the previous value (as a number).
    this.previousValue = parseFloat(this.currentInput);
    // Reset current input for the next number.
    this.currentInput = "0";
    this.updateDisplay();
  }

  /** Perform the pending arithmetic operation. */
  calculateResult() {
    if (this.operator === null || this.previousValue === null) {
      return; // Nothing to compute.
    }
    const current = parseFloat(this.currentInput);
    let result;
    switch (this.operator) {
      case "+":
        result = this.previousValue + current;
        break;
      case "-":
        result = this.previousValue - current;
        break;
      case "*":
        result = this.previousValue * current;
        break;
      case "/":
        // Guard against division by zero.
        result = current === 0 ? 0 : this.previousValue / current;
        break;
      default:
        result = current;
    }
    // Prepare for a new chain of operations.
    this.currentInput = result.toString();
    this.previousValue = null;
    this.operator = null;
    this.updateDisplay();
  }

  /** Convert the current input to a percentage (divide by 100). */
  calculatePercentage() {
    const value = parseFloat(this.currentInput) / 100;
    this.currentInput = value.toString();
    this.updateDisplay();
  }
}

// ---------------------------------------------------
// UI Wiring – connect button clicks to the Calculator instance.
const displayEl = document.getElementById("display");
const calculator = new Calculator(displayEl);

// Helper to safely get dataset values.
function getDataAttribute(element, name) {
  return element.dataset[name];
}

// Attach listeners to all calculator buttons.
document.querySelectorAll('.buttons button').forEach((btn) => {
  btn.addEventListener('click', () => {
    const action = getDataAttribute(btn, 'action');
    const value = getDataAttribute(btn, 'value');

    switch (action) {
      case 'number':
        calculator.inputDigit(value);
        break;
      case 'decimal':
        calculator.inputDecimal();
        break;
      case 'sign':
        calculator.toggleSign();
        break;
      case 'clear':
        // The UI only provides a single clear button (C). Treat it as all clear.
        calculator.allClear();
        break;
      case 'operator':
        calculator.setOperator(value);
        break;
      case 'equals':
        calculator.calculateResult();
        break;
      case 'percent':
        calculator.calculatePercentage();
        break;
      default:
        // No action – ignore.
        break;
    }
  });
});

// ---------------------------------------------------
// Keyboard support – map key presses to calculator actions.
// This listener works globally for the document.
document.addEventListener('keydown', (e) => {
  const key = e.key;
  // Numbers (both main keyboard and numpad produce the same key string).
  if (key >= '0' && key <= '9') {
    calculator.inputDigit(key);
    e.preventDefault();
    return;
  }

  switch (key) {
    case '.':
    case ',': // Some locales use comma for decimal.
      calculator.inputDecimal();
      e.preventDefault();
      break;
    case '+':
    case '-':
    case '*':
    case '/':
      calculator.setOperator(key);
      e.preventDefault();
      break;
    case 'Enter':
    case '=': // Allow '=' as alternative.
      calculator.calculateResult();
      e.preventDefault();
      break;
    case 'Backspace':
      calculator.clearEntry();
      e.preventDefault();
      break;
    case 'Escape':
      calculator.allClear();
      e.preventDefault();
      break;
    case '%':
      calculator.calculatePercentage();
      e.preventDefault();
      break;
    default:
      // Do nothing for other keys.
      break;
  }
});
