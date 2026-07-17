function SyntaxPage() {
    return (
        <div>

            {/* General */}
            <h2 id="general">
                General
            </h2>

            <p>
                RAMZ uses <code>;</code> to separate statements. New lines can also be used
                to separate statements.
            </p>

            <p>
                RAMZ uses block-based scopes. Conditional statements such as
                <code> if </code> and loops such as <code> while </code> create child scopes,
                allowing variables to be searched from the current scope through its parent
                scopes.
            </p>

            <p>
                Functions create an isolated scope. Variables inside functions cannot access
                variables from their outer scopes unless they are passed as parameters or
                explicitly provided by the language.
            </p>


            <p>
                RAMZ currently supports only single-file programs.
            </p>

            <p>
                For an overview of additional commands and compiler usage, check the compiler
                README.
            </p>

            {/* Comments */}
            <h2 id="comments" className="mt-5">
                Comments
            </h2>

            <p>
                RAMZ supports single-line and multi-line comments.
            </p>

            <ul>
                <li>
                    Single-line comments using <code>//</code> or <code>#</code>
                </li>

                <li>
                    Multi-line comments using <code>/* */</code>
                </li>
            </ul>



            {/* Output */}
            <h2 id="output" className="mt-5">
                Output
            </h2>

            <p>
                RAMZ supports the <code>print()</code> command and can handle all
                RAMZ datatypes.
            </p>



            {/* Datatypes */}
            <h2 id="datatypes" className="mt-5">
                Datatypes
            </h2>

            <p>
                RAMZ supports the following datatypes:
            </p>

            <ul>
                <li>
                    <code>int</code> — Integer numbers
                </li>

                <li>
                    <code>dec</code> — Decimal numbers
                </li>

                <li>
                    <code>str</code> — Strings
                </li>

                <li>
                    <code>bool</code> — Boolean values
                </li>

                <li>
                    <code>void</code> — Represents the absence of a value
                </li>
            </ul>



            {/* Strings */}
            <h3  className="mt-4">
                Strings
            </h3>

            <p>
                Strings in RAMZ can be represented using double quotes
                <code>" "</code>
                or single quotes
                <code>' '</code>.
                <br />
                They support multiline text and can contain new lines.
            </p>

            <p>
                RAMZ supports the following escape characters:
            </p>

            <ul>
                <li><code>\n</code> — New line</li>
                <li><code>\t</code> — Tab</li>
                <li><code>\r</code> — Carriage return</li>
                <li><code>\\</code> — Backslash</li>
                <li><code>\"</code> — Double quote</li>
                <li><code>\'</code> — Single quote</li>
                <li><code>\0</code> — Null character</li>
            </ul>


            {/* Variables */}
            <h2 id="variables" className="mt-5">
                Variables
            </h2>

            <p>
                RAMZ supports variable declaration, assignment, and reading.
            </p>

            <ul>
                <li>
                    Variables are declared using:
                    <br />
                    <code>var name = value;</code>
                </li>

                <li>
                    Variables can be assigned new values using:
                    <br />
                    <code>name = value;</code>
                </li>

                <li>
                    Variables can be read by using their name:
                    <br />
                    <code>name</code>
                </li>
            </ul>


            <h3 className="mt-4">
                Variable Rules
            </h3>

            <ul>
                <li>
                    A variable must be initialized with a value when declared to determine its datatype.
                </li>

                <li>
                    Variables must always store a value. A function that returns <code>void</code>
                    cannot be assigned to a variable.
                </li>

                <li>
                    A variable cannot be assigned a different datatype after declaration.
                </li>

                <li>
                    A variable cannot be redeclared in the same scope.
                </li>

                <li>
                    Variable names are case-sensitive.
                </li>

                <li>
                    Variable names cannot use reserved constant names.
                </li>

                <li>
                    Variable names can only contain letters and underscores (<code>_</code>).
                </li>
            </ul>


            <h3 className="mt-4">
                Example
            </h3>

            <pre className="bg-light border rounded p-3">
                {"var age = 20;\nage = 25;\n\nprint(age);"}
            </pre>


            <h3 id="variable-scope" className="mt-4">
                Variable Scope
            </h3>

            <p>
                When accessing a variable, RAMZ searches the current scope and its parent
                scopes until the closest declaration is found.
            </p>

            <p>
                This lookup applies to block scopes such as <code>if</code> statements and
                <code>while</code> loops. Function scopes are isolated and cannot access
                variables from their parent scopes.
            </p>


            <h3 id="scope-example" className="mt-4">
                Example
            </h3>

            <pre className="bg-light border rounded p-3">
                {"var x = 10;\n\nif (true) {\n    print(x); // uses the parent scope variable\n}\n\nwhile (condition) {\n    print(x); // uses the parent scope variable\n}\n\nfunction test() {\n    print(x); // invalid: functions have isolated scopes\n}"}
            </pre>

            {/* Constants */}
            <h2 id="constants" className="mt-5">
                Constants
            </h2>

            <p>
                RAMZ provides built-in constants that cannot be modified.
                Their values are replaced before compilation.
            </p>

            <p>
                Currently, RAMZ supports the following constants:
            </p>

            <ul>
                <li>
                    <code>INT_MAX</code> — Maximum value supported by the RAMZ integer datatype.
                </li>

                <li>
                    <code>INT_MIN</code> — Minimum value supported by the RAMZ integer datatype.
                </li>

                <li>
                    <code>DEC_MAX</code> — Maximum value supported by the RAMZ decimal datatype.
                </li>

                <li>
                    <code>DEC_MIN</code> — Minimum value supported by the RAMZ decimal datatype.
                </li>

                <li>
                    <code>HELLO_WORLD</code> — Returns a test string value.
                </li>
            </ul>


            <h3 className="mt-4">
                Constant Rules
            </h3>

            <ul>
                <li>
                    Constants cannot be assigned new values.
                </li>

                <li>
                    Constants are replaced with their values before compilation.
                </li>

                <li>
                    Constant names are reserved and cannot be used as variable names.
                </li>
            </ul>


            <h3 className="mt-4">
                Example
            </h3>

            <pre className="bg-light border rounded p-3">
                {"print(INT_MAX);\nprint(HELLO_WORLD);"}
            </pre>


            {/* Operations */}
            <h2 id="operations" className="mt-5">
                Operations
            </h2>

            <p>
                RAMZ supports unary operations, binary operations, comparisons, and logical
                operations.
            </p>


            <h3 className="mt-4">
                Unary Operations
            </h3>

            <p>
                Unary operations work on a single value.
            </p>

            <ul>
                <li>
                    Negation:
                    <br />
                    <code>-a</code> and <code>+a</code>
                </li>

                <li>
                    Logical NOT:
                    <br />
                    <code>!bool</code>
                </li>
            </ul>



            <h3 className="mt-4">
                Binary Operations
            </h3>

            <p>
                RAMZ supports the following arithmetic binary operations:
            </p>

            <ul>
                <li><code>+</code> Addition</li>
                <li><code>-</code> Subtraction</li>
                <li><code>*</code> Multiplication</li>
                <li><code>/</code> Division</li>
            </ul>

            <p>
                Arithmetic operations only work with <code>int</code> and <code>dec</code>
                values. Both operands must have the same datatype.
            </p>



            <h3 className="mt-4">
                Comparisons
            </h3>

            <p>
                Comparison operations return a <code>bool</code> value.
            </p>

            <ul>
                <li><code>==</code> Equal</li>
                <li><code>!=</code> Not equal</li>
                <li><code>&gt;</code> Greater than</li>
                <li><code>&lt;</code> Less than</li>
                <li><code>&gt;=</code> Greater than or equal</li>
                <li><code>&lt;=</code> Less than or equal</li>
            </ul>

            <p>
                Comparisons only support <code>int</code> and <code>dec</code> and <code>bool</code> values.
                Both sides of the comparison must have the same datatype.
            </p>



            <h3 className="mt-4">
                Logical Operations
            </h3>

            <p>
                RAMZ supports logical operations using boolean expressions.
            </p>

            <ul>
                <li>
                    AND:
                    <code>and</code>
                </li>

                <li>
                    OR:
                    <code>or</code>
                </li>
            </ul>

            <p>
                Logical operations only accept expressions that return a
                <code>bool</code> value. Parentheses <code>()</code> can be used to control
                evaluation order.
            </p>



            <h3 className="mt-4">
                Operator Precedence
            </h3>

            <p>
                RAMZ evaluates expressions in the following order:
            </p>

            <ol>
                <li>
                    Parentheses and single values:
                    <code>()</code>, variables, constants
                </li>

                <li>
                    Unary operations:
                    <code>!</code>, <code>+</code>, <code>-</code>
                </li>

                <li>
                    Multiplication and division:
                    <code>*</code>, <code>/</code>
                </li>

                <li>
                    Addition and subtraction:
                    <code>+</code>, <code>-</code>
                </li>

                <li>
                    Comparisons:
                    <code>== != &gt; &lt; &gt;= &lt;=</code>
                </li>

                <li>
                    Logical AND:
                    <code>and</code>
                </li>

                <li>
                    Logical OR:
                    <code>or</code>
                </li>
            </ol>

            {/* Conditional Statements */}
            <h2 id="conditional-statements" className="mt-5">
                Conditional Statements
            </h2>

            <p>
                RAMZ supports conditional execution using <code>if</code>, <code>elif</code>,
                and <code>else</code> statements.
            </p>

            <ul>
                <li>
                    An <code>if</code> statement requires an expression that evaluates to
                    <code>true</code>.
                </li>

                <li>
                    Any number of <code>elif</code> blocks can be added after an
                    <code>if</code> statement.
                </li>

                <li>
                    An optional <code>else</code> block can be added at the end.
                </li>

                <li>
                    <code>if</code>, <code>elif</code>, and <code>else</code> blocks cannot be
                    separated using <code>;</code>.
                </li>
            </ul>


            <h3 className="mt-4">
                Example
            </h3>

            <pre className="bg-light border rounded p-3">
                {"if (age >= 18) {\n    print(\"Adult\");\n}\nelif (age > 12) {\n    print(\"Teen\");\n}\nelse {\n    print(\"Child\");\n}"}
            </pre>


            {/* Loops */}
            <h2 id="loops" className="mt-5">
                Loops
            </h2>

            <p>
                RAMZ currently supports the <code>while</code> loop for repeated execution.
            </p>

            <ul>
                <li>
                    A <code>while</code> loop requires an expression that evaluates to
                    <code>bool</code>.
                </li>

                <li>
                    The loop continues executing while the expression returns
                    <code>true</code>.
                </li>

                <li>
                    The loop body creates its own block scope.
                </li>
            </ul>


            <h3 className="mt-4">
                While Loop
            </h3>

            <p>
                A <code>while</code> loop uses the following syntax:
            </p>

            <pre className="bg-light border rounded p-3">
                {"while (condition) {\n    // code\n}"}
            </pre>


            <h3 className="mt-4">
                Infinite Loops
            </h3>

            <p>
                If an infinite loop occurs, the program can be stopped using
                <code>Ctrl + C</code> or by running the <code>ramz kill</code> command
                from another terminal.
            </p>

            {/* Functions */}
            <h2 id="functions" className="mt-5">
                Functions
            </h2>

            <p>
                RAMZ supports user-defined functions. Functions can return a value or be used
                only for execution without returning a value.
            </p>


            <h3 className="mt-4">
                Function Declaration
            </h3>

            <p>
                Functions are declared using the following syntax:
            </p>

            <pre className="bg-light border rounded p-3">
                {"function name datatype(parameters) {\n    return value;\n}"}
            </pre>

            <ul>
                <li>
                    The function datatype specifies the return type.
                </li>

                <li>
                    If no datatype is provided, the function datatype is automatically set
                    to <code>void</code>.
                </li>

                <li>
                    A <code>void</code> function cannot contain a <code>return</code>
                    statement.
                </li>
            </ul>



            <h3 className="mt-4">
                Function Rules
            </h3>

            <ul>
                <li>
                    A function can currently contain only one <code>return</code> statement.
                </li>

                <li>
                    Function parameters get their datatypes from the first function call.
                </li>

                <li>
                    If a function is never called, its parameters are automatically assigned
                    the <code>int</code> datatype.
                </li>

                <li>
                    The number of arguments passed during a function call must match the
                    number of parameters.
                </li>

                <li>
                    Variables inside functions are isolated and cannot access variables from
                    parent scopes.
                </li>
            </ul>



            <h3 className="mt-4">
                Function Calling
            </h3>

            <p>
                Functions are called using the function name followed by its arguments:
            </p>

            <pre className="bg-light border rounded p-3">
                {"name(1, 2, 3);"}
            </pre>

            <ul>
                <li>
                    Function calls search the current function scope and parent function
                    scopes for the closest matching function declaration.
                </li>

                <li>
                    Function lookup is different from variable lookup.
                </li>
            </ul>



            <h3 className="mt-4">
                Nested Functions
            </h3>

            <p>
                Functions can be declared inside other functions and can be called from
                their containing function scope.
            </p>

            <pre className="bg-light border rounded p-3">
                {"function main void() {\n    function hello void() {\n        print(\"Hello\");\n    }\n\n    hello();\n}"}
            </pre>



            <h3 className="mt-4">
                Current Limitations
            </h3>

            <ul>
                <li>
                    The <code>return</code> statement must be placed at the end of the
                    function.
                </li>

                <li>
                    Recursive function calls are currently disabled.
                </li>

                <li>
                    A function cannot call itself directly or indirectly.
                </li>
            </ul>


        </div>
    );
}

export default SyntaxPage;