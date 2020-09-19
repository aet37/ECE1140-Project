# Group 4 C++ Coding Standard

<h2 id="Header_Files">Header Files</h2>

<p>In general, every <code>.cpp</code> file should have an
associated <code>.h</code> file. There are some common
exceptions, such as unit tests and small <code>.cpp</code> files containing
just a <code>main()</code> function.</p>

<p>Correct use of header files can make a huge difference to
the readability, size and performance of your code.</p>

<p>The following rules will guide you through the various
pitfalls of using header files.</p>

<a id="The_-inl.h_Files"></a>
<h3 id="Self_contained_Headers">Self-contained Headers</h3>

<p>Header files should be self-contained (compile on their own) and
end in <code>.h</code>.  Non-header files that are meant for inclusion
should end in <code>.inc</code> and be used sparingly.</p>

<p>All header files should be self-contained. Users and refactoring
tools should not have to adhere to special conditions to include the
header. Specifically, a header should
have <a href="#The__define_Guard">header guards</a> and include all
other headers it needs.</p>

<p>Prefer placing the definitions for template and inline functions in
the same file as their declarations.  The definitions of these
constructs must be included into every <code>.cc</code> file that uses
them, or the program may fail to link in some build configurations.  If
declarations and definitions are in different files, including the
former should transitively include the latter.  Do not move these
definitions to separately included header files (<code>-inl.h</code>);
this practice was common in the past, but is no longer allowed.</p>

<p>As an exception, a template that is explicitly instantiated for
all relevant sets of template arguments, or that is a private
implementation detail of a class, is allowed to be defined in the one
and only <code>.cc</code> file that instantiates the template.</p>

<p>There are rare cases where a file designed to be included is not
self-contained.  These are typically intended to be included at unusual
locations, such as the middle of another file.  They might not
use <a href="#The__define_Guard">header guards</a>, and might not include
their prerequisites.  Name such files with the <code>.inc</code>
extension.  Use sparingly, and prefer self-contained headers when
possible.</p>

<h3 id="The__define_Guard">The #define Guard</h3>

<p>All header files should have <code>#define</code> guards to
prevent multiple inclusion. The format of the symbol name
should be

<code><i>&lt;PROJECT&gt;</i>_<i>&lt;PATH&gt;</i>_<i>&lt;FILE&gt;</i>_H_</code>.</p>



<div>
<p>To guarantee uniqueness, they should
be based on the full path in a project's source tree. For
example, the file <code>foo/src/bar/baz.h</code> in
project <code>foo</code> should have the following
guard:</p>
</div>

<pre>#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_

...

#endif  // FOO_BAR_BAZ_H_
</pre>



<h3 id="Forward_Declarations">Forward Declarations</h3>

<p>Avoid using forward declarations where possible.
Instead, <code>#include</code> the headers you need.</p>

<p class="definition"></p>
<p>A "forward declaration" is a declaration of a class,
function, or template without an associated definition.</p>

<p class="pros"></p>
<ul>
  <li>Forward declarations can save compile time, as
  <code>#include</code>s force the compiler to open
  more files and process more input.</li>

  <li>Forward declarations can save on unnecessary
  recompilation. <code>#include</code>s can force
  your code to be recompiled more often, due to unrelated
  changes in the header.</li>
</ul>

<p class="cons"></p>
<ul>
  <li>Forward declarations can hide a dependency, allowing
  user code to skip necessary recompilation when headers
  change.</li>

  <li>A forward declaration may be broken by subsequent
  changes to the library. Forward declarations of functions
  and templates can prevent the header owners from making
  otherwise-compatible changes to their APIs, such as
  widening a parameter type, adding a template parameter
  with a default value, or migrating to a new namespace.</li>

  <li>Forward declaring symbols from namespace
  <code>std::</code> yields undefined behavior.</li>

  <li>It can be difficult to determine whether a forward
  declaration or a full <code>#include</code> is needed.
  Replacing an <code>#include</code> with a forward
  declaration can silently change the meaning of
  code:
<pre>// b.h:
struct B {};
struct D : B {};

// good_user.cc:
#include "b.h"
void f(B*);
void f(void*);
void test(D* x) { f(x); }  // calls f(B*)
</pre>
  If the <code>#include</code> was replaced with forward
  decls for <code>B</code> and <code>D</code>,
  <code>test()</code> would call <code>f(void*)</code>.
  </li>

  <li>Forward declaring multiple symbols from a header
  can be more verbose than simply
  <code>#include</code>ing the header.</li>

  <li>Structuring code to enable forward declarations
  (e.g., using pointer members instead of object members)
  can make the code slower and more complex.</li>


</ul>

<p class="decision"></p>
<ul>
  <li>Try to avoid forward declarations of entities
  defined in another project.</li>

  <li>When using a function declared in a header file,
  always <code>#include</code> that header.</li>

  <li>When using a class template, prefer to
  <code>#include</code> its header file.</li>
</ul>

<p>Please see <a href="#Names_and_Order_of_Includes">Names and Order
of Includes</a> for rules about when to #include a header.</p>

<h3 id="Inline_Functions">Inline Functions</h3>

<p>Define functions inline only when they are small, say, 10
lines or fewer.</p>

<p class="definition"></p>
<p>You can declare functions in a way that allows the compiler to expand
them inline rather than calling them through the usual
function call mechanism.</p>

<p class="pros"></p>
<p>Inlining a function can generate more efficient object
code, as long as the inlined function is small. Feel free
to inline accessors and mutators, and other short,
performance-critical functions.</p>

<p class="cons"></p>
<p>Overuse of inlining can actually make programs slower.
Depending on a function's size, inlining it can cause the
code size to increase or decrease. Inlining a very small
accessor function will usually decrease code size while
inlining a very large function can dramatically increase
code size. On modern processors smaller code usually runs
faster due to better use of the instruction cache.</p>

<p class="decision"></p>
<p>A decent rule of thumb is to not inline a function if
it is more than 10 lines long. Beware of destructors,
which are often longer than they appear because of
implicit member- and base-destructor calls!</p>

<p>Another useful rule of thumb: it's typically not cost
effective to inline functions with loops or switch
statements (unless, in the common case, the loop or
switch statement is never executed).</p>

<p>It is important to know that functions are not always
inlined even if they are declared as such; for example,
virtual and recursive functions are not normally inlined.
Usually recursive functions should not be inline. The
main reason for making a virtual function inline is to
place its definition in the class, either for convenience
or to document its behavior, e.g., for accessors and
mutators.</p>

<h3 id="Names_and_Order_of_Includes">Names and Order of Includes</h3>

<p>Include headers in the following order: Related header, C system headers,
C++ standard library headers,
other libraries' headers, your project's
headers.</p>

<p>
All of a project's header files should be
listed as descendants of the project's source
directory without use of UNIX directory aliases
<code>.</code> (the current directory) or <code>..</code>
(the parent directory). For example,

<code>google-awesome-project/src/base/logging.h</code>
should be included as:</p>

<pre>#include "base/logging.h"
</pre>

<p>In <code><var>dir/foo</var>.cc</code> or
<code><var>dir/foo_test</var>.cc</code>, whose main
purpose is to implement or test the stuff in
<code><var>dir2/foo2</var>.h</code>, order your includes
as follows:</p>

<ol>
  <li><code><var>dir2/foo2</var>.h</code>.</li>

  <li>A blank line</li>

  <li>C system headers (more precisely: headers in angle brackets with the
    <code>.h</code> extension), e.g., <code>&lt;unistd.h&gt;</code>,
    <code>&lt;stdlib.h&gt;</code>.</li>

  <li>A blank line</li>

  <li>C++ standard library headers (without file extension), e.g.,
    <code>&lt;algorithm&gt;</code>, <code>&lt;cstddef&gt;</code>.</li>

  <li>A blank line</li>

  <div>
  <li>Other libraries' <code>.h</code> files.</li>
  </div>

  <li>
  Your project's <code>.h</code>
  files.</li>
</ol>

<p>Separate each non-empty group with one blank line.</p>

<p>With the preferred ordering, if the related header
<code><var>dir2/foo2</var>.h</code> omits any necessary
includes, the build of <code><var>dir/foo</var>.cc</code>
or <code><var>dir/foo</var>_test.cc</code> will break.
Thus, this rule ensures that build breaks show up first
for the people working on these files, not for innocent
people in other packages.</p>

<p><code><var>dir/foo</var>.cc</code> and
<code><var>dir2/foo2</var>.h</code> are usually in the same
directory (e.g., <code>base/basictypes_test.cc</code> and
<code>base/basictypes.h</code>), but may sometimes be in different
directories too.</p>



<p>Note that the C headers such as <code>stddef.h</code>
are essentially interchangeable with their C++ counterparts
(<code>cstddef</code>).
Either style is acceptable, but prefer consistency with existing code.</p>

<p>Within each section the includes should be ordered
alphabetically. Note that older code might not conform to
this rule and should be fixed when convenient.</p>

<p>You should include all the headers that define the symbols you rely
upon, except in the unusual case of <a href="#Forward_Declarations">forward
declaration</a>. If you rely on symbols from <code>bar.h</code>,
don't count on the fact that you included <code>foo.h</code> which
(currently) includes <code>bar.h</code>: include <code>bar.h</code>
yourself, unless <code>foo.h</code> explicitly demonstrates its intent
to provide you the symbols of <code>bar.h</code>.</p>

<p>For example, the includes in

<code>google-awesome-project/src/foo/internal/fooserver.cc</code>
might look like this:</p>

<pre>#include "foo/server/fooserver.h"

#include &lt;sys/types.h&gt;
#include &lt;unistd.h&gt;

#include &lt;string&gt;
#include &lt;vector&gt;

#include "base/basictypes.h"
#include "base/commandlineflags.h"
#include "foo/server/bar.h"
</pre>

<p><b>Exception:</b></p>

<p>Sometimes, system-specific code needs
conditional includes. Such code can put conditional
includes after other includes. Of course, keep your
system-specific code small and localized. Example:</p>

<pre>#include "foo/public/fooserver.h"

#include "base/port.h"  // For LANG_CXX11.

#ifdef LANG_CXX11
#include &lt;initializer_list&gt;
#endif  // LANG_CXX11
</pre>

<h2 id="Scoping">Scoping</h2>

<h3 id="Namespaces">Namespaces</h3>

<p>With few exceptions, place code in a namespace. Namespaces
should have unique names based on the project name, and possibly
its path. Do not use <i>using-directives</i> (e.g.,
<code>using namespace foo</code>). Do not use
inline namespaces. For unnamed namespaces, see
<a href="#Unnamed_Namespaces_and_Static_Variables">Unnamed Namespaces and
Static Variables</a>.

</p><p class="definition"></p>
<p>Namespaces subdivide the global scope
into distinct, named scopes, and so are useful for preventing
name collisions in the global scope.</p>

<p class="pros"></p>

<p>Namespaces provide a method for preventing name conflicts
in large programs while allowing most code to use reasonably
short names.</p>

<p>For example, if two different projects have a class
<code>Foo</code> in the global scope, these symbols may
collide at compile time or at runtime. If each project
places their code in a namespace, <code>project1::Foo</code>
and <code>project2::Foo</code> are now distinct symbols that
do not collide, and code within each project's namespace
can continue to refer to <code>Foo</code> without the prefix.</p>

<p>Inline namespaces automatically place their names in
the enclosing scope. Consider the following snippet, for
example:</p>

<pre class="neutralcode">namespace outer {
inline namespace inner {
  void foo();
}  // namespace inner
}  // namespace outer
</pre>

<p>The expressions <code>outer::inner::foo()</code> and
<code>outer::foo()</code> are interchangeable. Inline
namespaces are primarily intended for ABI compatibility
across versions.</p>

<p class="cons"></p>

<p>Namespaces can be confusing, because they complicate
the mechanics of figuring out what definition a name refers
to.</p>

<p>Inline namespaces, in particular, can be confusing
because names aren't actually restricted to the namespace
where they are declared. They are only useful as part of
some larger versioning policy.</p>

<p>In some contexts, it's necessary to repeatedly refer to
symbols by their fully-qualified names. For deeply-nested
namespaces, this can add a lot of clutter.</p>

<p class="decision"></p>

<p>Namespaces should be used as follows:</p>

<ul>
  <li>Follow the rules on <a href="#Namespace_Names">Namespace Names</a>.
  </li><li>Terminate namespaces with comments as shown in the given examples.
  </li><li>

  <p>Namespaces wrap the entire source file after
  includes,
  <a href="https://gflags.github.io/gflags/">
  gflags</a> definitions/declarations
  and forward declarations of classes from other namespaces.</p>

<pre>// In the .h file
namespace mynamespace {

// All declarations are within the namespace scope.
// Notice the lack of indentation.
class MyClass {
 public:
  ...
  void Foo();
};

}  // namespace mynamespace
</pre>

<pre>// In the .cc file
namespace mynamespace {

// Definition of functions is within scope of the namespace.
void MyClass::Foo() {
  ...
}

}  // namespace mynamespace
</pre>

  <p>More complex <code>.cc</code> files might have additional details,
  like flags or using-declarations.</p>

<pre>#include "a.h"

ABSL_FLAG(bool, someflag, false, "dummy flag");

namespace mynamespace {

using ::foo::Bar;

...code for mynamespace...    // Code goes against the left margin.

}  // namespace mynamespace
</pre>
  </li>

  <li>To place generated protocol
  message code in a namespace, use the
  <code>package</code> specifier in the
  <code>.proto</code> file. See


  <a href="https://developers.google.com/protocol-buffers/docs/reference/cpp-generated#package">
  Protocol Buffer Packages</a>
  for details.</li>

  <li>Do not declare anything in namespace
  <code>std</code>, including forward declarations of
  standard library classes. Declaring entities in
  namespace <code>std</code> is undefined behavior, i.e.,
  not portable. To declare entities from the standard
  library, include the appropriate header file.</li>

  <li><p>You may not use a <i>using-directive</i>
  to make all names from a namespace available.</p>

<pre class="badcode">// Forbidden -- This pollutes the namespace.
using namespace foo;
</pre>
  </li>

  <li><p>Do not use <i>Namespace aliases</i> at namespace scope
  in header files except in explicitly marked
  internal-only namespaces, because anything imported into a namespace
  in a header file becomes part of the public
  API exported by that file.</p>

<pre>// Shorten access to some commonly used names in .cc files.
namespace baz = ::foo::bar::baz;
</pre>

<pre>// Shorten access to some commonly used names (in a .h file).
namespace librarian {
namespace impl {  // Internal, not part of the API.
namespace sidetable = ::pipeline_diagnostics::sidetable;
}  // namespace impl

inline void my_inline_function() {
  // namespace alias local to a function (or method).
  namespace baz = ::foo::bar::baz;
  ...
}
}  // namespace librarian
</pre>

  </li><li>Do not use inline namespaces.</li>
</ul>

<h3 id="Unnamed_Namespaces_and_Static_Variables">Unnamed Namespaces and Static
Variables</h3>

<p>When definitions in a <code>.cc</code> file do not need to be
referenced outside that file, place them in an unnamed
namespace or declare them <code>static</code>. Do not use either
of these constructs in <code>.h</code> files.

</p><p class="definition"></p>
<p>All declarations can be given internal linkage by placing them in unnamed
namespaces. Functions and variables can also be given internal linkage by
declaring them <code>static</code>. This means that anything you're declaring
can't be accessed from another file. If a different file declares something with
the same name, then the two entities are completely independent.</p>

<p class="decision"></p>

<p>Use of internal linkage in <code>.cc</code> files is encouraged
for all code that does not need to be referenced elsewhere.
Do not use internal linkage in <code>.h</code> files.</p>

<p>Format unnamed namespaces like named namespaces. In the
  terminating comment, leave the namespace name empty:</p>

<pre>namespace {
...
}  // namespace
</pre>

<h3 id="Nonmember,_Static_Member,_and_Global_Functions">Nonmember, Static Member, and Global Functions</h3>

<p>Prefer placing nonmember functions in a namespace; use completely global
functions rarely. Do not use a class simply to group static members. Static
methods of a class should generally be closely related to instances of the
class or the class's static data.</p>


<p class="pros"></p>
<p>Nonmember and static member functions can be useful in
some situations. Putting nonmember functions in a
namespace avoids polluting the global namespace.</p>

<p class="cons"></p>
<p>Nonmember and static member functions may make more sense
as members of a new class, especially if they access
external resources or have significant dependencies.</p>

<p class="decision"></p>
<p>Sometimes it is useful to define a
function not bound to a class instance. Such a function
can be either a static member or a nonmember function.
Nonmember functions should not depend on external
variables, and should nearly always exist in a namespace.
Do not create classes only to group static members;
this is no different than just giving the names a
common prefix, and such grouping is usually unnecessary anyway.</p>

<p>If you define a nonmember function and it is only
needed in its <code>.cc</code> file, use
<a href="#Unnamed_Namespaces_and_Static_Variables">internal linkage</a> to limit
its scope.</p>

<h3 id="Local_Variables">Local Variables</h3>

<p>Place a function's variables in the narrowest scope
possible, and initialize variables in the declaration.</p>

<p>C++ allows you to declare variables anywhere in a
function. We encourage you to declare them in as local a
scope as possible, and as close to the first use as
possible. This makes it easier for the reader to find the
declaration and see what type the variable is and what it
was initialized to. In particular, initialization should
be used instead of declaration and assignment, e.g.,:</p>

<pre class="badcode">int i;
i = f();      // Bad -- initialization separate from declaration.
</pre>

<pre>int j = g();  // Good -- declaration has initialization.
</pre>

<pre class="badcode">std::vector&lt;int&gt; v;
v.push_back(1);  // Prefer initializing using brace initialization.
v.push_back(2);
</pre>

<pre>std::vector&lt;int&gt; v = {1, 2};  // Good -- v starts initialized.
</pre>

<p>Variables needed for <code>if</code>, <code>while</code>
and <code>for</code> statements should normally be declared
within those statements, so that such variables are confined
to those scopes.  E.g.:</p>

<pre>while (const char* p = strchr(str, '/')) str = p + 1;
</pre>

<p>There is one caveat: if the variable is an object, its
constructor is invoked every time it enters scope and is
created, and its destructor is invoked every time it goes
out of scope.</p>

<pre class="badcode">// Inefficient implementation:
for (int i = 0; i &lt; 1000000; ++i) {
  Foo f;  // My ctor and dtor get called 1000000 times each.
  f.DoSomething(i);
}
</pre>

<p>It may be more efficient to declare such a variable
used in a loop outside that loop:</p>

<pre>Foo f;  // My ctor and dtor get called once each.
for (int i = 0; i &lt; 1000000; ++i) {
  f.DoSomething(i);
}
</pre>

<h3 id="Static_and_Global_Variables">Static and Global Variables</h3>

<p>Objects with
<a href="http://en.cppreference.com/w/cpp/language/storage_duration#Storage_duration">
static storage duration</a> are forbidden unless they are
<a href="http://en.cppreference.com/w/cpp/types/is_destructible">trivially
destructible</a>. Informally this means that the destructor does not do
anything, even taking member and base destructors into account. More formally it
means that the type has no user-defined or virtual destructor and that all bases
and non-static members are trivially destructible.
Static function-local variables may use dynamic initialization.
Use of dynamic initialization for static class member variables or variables at
namespace scope is discouraged, but allowed in limited circumstances; see below
for details.</p>

<p>As a rule of thumb: a global variable satisfies these requirements if its
declaration, considered in isolation, could be <code>constexpr</code>.</p>

<p class="definition"></p>
<p>Every object has a <dfn>storage duration</dfn>, which correlates with its
lifetime. Objects with static storage duration live from the point of their
initialization until the end of the program. Such objects appear as variables at
namespace scope ("global variables"), as static data members of classes, or as
function-local variables that are declared with the <code>static</code>
specifier. Function-local static variables are initialized when control first
passes through their declaration; all other objects with static storage duration
are initialized as part of program start-up. All objects with static storage
duration are destroyed at program exit (which happens before unjoined threads
are terminated).</p>

<p>Initialization may be <dfn>dynamic</dfn>, which means that something
non-trivial happens during initialization. (For example, consider a constructor
that allocates memory, or a variable that is initialized with the current
process ID.) The other kind of initialization is <dfn>static</dfn>
initialization. The two aren't quite opposites, though: static
initialization <em>always</em> happens to objects with static storage duration
(initializing the object either to a given constant or to a representation
consisting of all bytes set to zero), whereas dynamic initialization happens
after that, if required.</p>

<p class="pros"></p>
<p>Global and static variables are very useful for a large number of
applications: named constants, auxiliary data structures internal to some
translation unit, command-line flags, logging, registration mechanisms,
background infrastructure, etc.</p>

<p class="cons"></p>
<p>Global and static variables that use dynamic initialization or have
non-trivial destructors create complexity that can easily lead to hard-to-find
bugs. Dynamic initialization is not ordered across translation units, and
neither is destruction (except that destruction
happens in reverse order of initialization). When one initialization refers to
another variable with static storage duration, it is possible that this causes
an object to be accessed before its lifetime has begun (or after its lifetime
has ended). Moreover, when a program starts threads that are not joined at exit,
those threads may attempt to access objects after their lifetime has ended if
their destructor has already run.</p>

<p class="decision"></p>
<h4>Decision on destruction</h4>

<p>When destructors are trivial, their execution is not subject to ordering at
all (they are effectively not "run"); otherwise we are exposed to the risk of
accessing objects after the end of their lifetime. Therefore, we only allow
objects with static storage duration if they are trivially destructible.
Fundamental types (like pointers and <code>int</code>) are trivially
destructible, as are arrays of trivially destructible types. Note that
variables marked with <code>constexpr</code> are trivially destructible.</p>
<pre>const int kNum = 10;  // allowed

struct X { int n; };
const X kX[] = {{1}, {2}, {3}};  // allowed

void foo() {
  static const char* const kMessages[] = {"hello", "world"};  // allowed
}

// allowed: constexpr guarantees trivial destructor
constexpr std::array&lt;int, 3&gt; kArray = {{1, 2, 3}};</pre>
<pre class="badcode">// bad: non-trivial destructor
const std::string kFoo = "foo";

// bad for the same reason, even though kBar is a reference (the
// rule also applies to lifetime-extended temporary objects)
const std::string&amp; kBar = StrCat("a", "b", "c");

void bar() {
  // bad: non-trivial destructor
  static std::map&lt;int, int&gt; kData = {{1, 0}, {2, 0}, {3, 0}};
}</pre>

<p>Note that references are not objects, and thus they are not subject to the
constraints on destructibility. The constraint on dynamic initialization still
applies, though. In particular, a function-local static reference of the form
<code>static T&amp; t = *new T;</code> is allowed.</p>

<h4>Decision on initialization</h4>

<p>Initialization is a more complex topic. This is because we must not only
consider whether class constructors execute, but we must also consider the
evaluation of the initializer:</p>
<pre class="neutralcode">int n = 5;    // fine
int m = f();  // ? (depends on f)
Foo x;        // ? (depends on Foo::Foo)
Bar y = g();  // ? (depends on g and on Bar::Bar)
</pre>

<p>All but the first statement expose us to indeterminate initialization
ordering.</p>

<p>The concept we are looking for is called <em>constant initialization</em> in
the formal language of the C++ standard. It means that the initializing
expression is a constant expression, and if the object is initialized by a
constructor call, then the constructor must be specified as
<code>constexpr</code>, too:</p>
<pre>struct Foo { constexpr Foo(int) {} };

int n = 5;  // fine, 5 is a constant expression
Foo x(2);   // fine, 2 is a constant expression and the chosen constructor is constexpr
Foo a[] = { Foo(1), Foo(2), Foo(3) };  // fine</pre>

<p>Constant initialization is always allowed. Constant initialization of
static storage duration variables should be marked with <code>constexpr</code>
or where possible the


<a href="https://github.com/abseil/abseil-cpp/blob/03c1513538584f4a04d666be5eb469e3979febba/absl/base/attributes.h#L540">
<code>ABSL_CONST_INIT</code></a>
attribute. Any non-local static storage
duration variable that is not so marked should be presumed to have
dynamic initialization, and reviewed very carefully.</p>

<p>By contrast, the following initializations are problematic:</p>

<pre class="badcode">// Some declarations used below.
time_t time(time_t*);      // not constexpr!
int f();                   // not constexpr!
struct Bar { Bar() {} };

// Problematic initializations.
time_t m = time(nullptr);  // initializing expression not a constant expression
Foo y(f());                // ditto
Bar b;                     // chosen constructor Bar::Bar() not constexpr</pre>

<p>Dynamic initialization of nonlocal variables is discouraged, and in general
it is forbidden. However, we do permit it if no aspect of the program depends
on the sequencing of this initialization with respect to all other
initializations. Under those restrictions, the ordering of the initialization
does not make an observable difference. For example:</p>
<pre>int p = getpid();  // allowed, as long as no other static variable
                   // uses p in its own initialization</pre>

<p>Dynamic initialization of static local variables is allowed (and common).</p>



<h4>Common patterns</h4>

<ul>
  <li>Global strings: if you require a global or static string constant,
    consider using a simple character array, or a char pointer to the first
    element of a string literal. String literals have static storage duration
    already and are usually sufficient.</li>
  <li>Maps, sets, and other dynamic containers: if you require a static, fixed
    collection, such as a set to search against or a lookup table, you cannot
    use the dynamic containers from the standard library as a static variable,
    since they have non-trivial destructors. Instead, consider a simple array of
    trivial types, e.g., an array of arrays of ints (for a "map from int to
    int"), or an array of pairs (e.g., pairs of <code>int</code> and <code>const
    char*</code>). For small collections, linear search is entirely sufficient
    (and efficient, due to memory locality); consider using the facilities from

    <a href="https://github.com/abseil/abseil-cpp/blob/master/absl/algorithm/container.h">absl/algorithm/container.h</a>


    for the standard operations. If necessary, keep the collection in sorted
    order and use a binary search algorithm. If you do really prefer a dynamic
    container from the standard library, consider using a function-local static
    pointer, as described below.</li>
  <li>Smart pointers (<code>unique_ptr</code>, <code>shared_ptr</code>): smart
    pointers execute cleanup during destruction and are therefore forbidden.
    Consider whether your use case fits into one of the other patterns described
    in this section. One simple solution is to use a plain pointer to a
    dynamically allocated object and never delete it (see last item).</li>
  <li>Static variables of custom types: if you require static, constant data of
    a type that you need to define yourself, give the type a trivial destructor
    and a <code>constexpr</code> constructor.</li>
  <li>If all else fails, you can create an object dynamically and never delete
    it by using a function-local static pointer or reference (e.g., <code>static
    const auto&amp; impl = *new T(args...);</code>).</li>
</ul>

<h2 id="Classes">Classes</h2>

<p>Classes are the fundamental unit of code in C++. Naturally,
we use them extensively. This section lists the main dos and
don'ts you should follow when writing a class.</p>

<h3 id="Doing_Work_in_Constructors">Doing Work in Constructors</h3>

<p>Avoid virtual method calls in constructors, and avoid
initialization that can fail if you can't signal an error.</p>

<p class="definition"></p>
<p>It is possible to perform arbitrary initialization in the body
of the constructor.</p>

<p class="pros"></p>
<ul>
  <li>No need to worry about whether the class has been initialized or
  not.</li>

  <li>Objects that are fully initialized by constructor call can
  be <code>const</code> and may also be easier to use with standard containers
  or algorithms.</li>
</ul>

<p class="cons"></p>
<ul>
  <li>If the work calls virtual functions, these calls
  will not get dispatched to the subclass
  implementations. Future modification to your class can
  quietly introduce this problem even if your class is
  not currently subclassed, causing much confusion.</li>

  <li>There is no easy way for constructors to signal errors, short of
  crashing the program (not always appropriate) or using exceptions
  (which are <a href="#Exceptions">forbidden</a>).</li>

  <li>If the work fails, we now have an object whose initialization
  code failed, so it may be an unusual state requiring a <code>bool
  IsValid()</code> state checking mechanism (or similar) which is easy
  to forget to call.</li>

  <li>You cannot take the address of a constructor, so whatever work
  is done in the constructor cannot easily be handed off to, for
  example, another thread.</li>
</ul>

<p class="decision"></p>
<p>Constructors should never call virtual functions. If appropriate
for your code ,
terminating the program may be an appropriate error handling
response. Otherwise, consider a factory function
or <code>Init()</code> method as described in
<a href="https://abseil.io/tips/42">TotW #42</a>
.
Avoid <code>Init()</code> methods on objects with
no other states that affect which public methods may be called
(semi-constructed objects of this form are particularly hard to work
with correctly).</p>

<h3 id="Structs_vs._Classes">Structs vs. Classes</h3>

<p>Use a <code>struct</code> only for passive objects that
      carry data; everything else is a <code>class</code>.</p>

<p>The <code>struct</code> and <code>class</code>
keywords behave almost identically in C++. We add our own
semantic meanings to each keyword, so you should use the
appropriate keyword for the data-type you're
defining.</p>

<p><code>structs</code> should be used for passive objects that carry
data, and may have associated constants. All fields must be public. The
struct must not have invariants that imply relationships between
different fields, since direct user access to those fields may
break those invariants. Constructors, destructors, and helper methods may
be present; however, these methods must not require or enforce any
invariants.</p>

<p>If more functionality or invariants are required, a
<code>class</code> is more appropriate. If in doubt, make
it a <code>class</code>.</p>

<p>For consistency with STL, you can use
<code>struct</code> instead of <code>class</code> for
stateless types, such as traits,
<a href="#Template_metaprogramming">template metafunctions</a>,
and some functors.</p>

<p>Note that member variables in structs and classes have
<a href="#Variable_Names">different naming rules</a>.</p>

<a id="Multiple_Inheritance"></a>
<h3 id="Inheritance">Inheritance</h3>

<p>Composition is often more appropriate than inheritance.
When using inheritance, make it <code>public</code>.</p>

<p class="definition"></p>
<p> When a sub-class
inherits from a base class, it includes the definitions
of all the data and operations that the base class
defines. "Interface inheritance" is inheritance from a
pure abstract base class (one with no state or defined
methods); all other inheritance is "implementation
inheritance".</p>

<p class="pros"></p>
<p>Implementation inheritance reduces code size by re-using
the base class code as it specializes an existing type.
Because inheritance is a compile-time declaration, you
and the compiler can understand the operation and detect
errors. Interface inheritance can be used to
programmatically enforce that a class expose a particular
API. Again, the compiler can detect errors, in this case,
when a class does not define a necessary method of the
API.</p>

<p class="cons"></p>
<p>For implementation inheritance, because the code
implementing a sub-class is spread between the base and
the sub-class, it can be more difficult to understand an
implementation. The sub-class cannot override functions
that are not virtual, so the sub-class cannot change
implementation.</p>

<p>Multiple inheritance is especially problematic, because
it often imposes a higher performance overhead (in fact,
the performance drop from single inheritance to multiple
inheritance can often be greater than the performance
drop from ordinary to virtual dispatch), and because
it risks leading to "diamond" inheritance patterns,
which are prone to ambiguity, confusion, and outright bugs.</p>

<p class="decision"></p>

<p>All inheritance should be <code>public</code>. If you
want to do private inheritance, you should be including
an instance of the base class as a member instead.</p>

<p>Do not overuse implementation inheritance. Composition
is often more appropriate. Try to restrict use of
inheritance to the "is-a" case: <code>Bar</code>
subclasses <code>Foo</code> if it can reasonably be said
that <code>Bar</code> "is a kind of"
<code>Foo</code>.</p>

<p>Limit the use of <code>protected</code> to those
member functions that might need to be accessed from
subclasses. Note that <a href="#Access_Control">data
members should be private</a>.</p>

<p>Explicitly annotate overrides of virtual functions or virtual
destructors with exactly one of an <code>override</code> or (less
frequently) <code>final</code> specifier. Do not
use <code>virtual</code> when declaring an override.
Rationale: A function or destructor marked
<code>override</code> or <code>final</code> that is
not an override of a base class virtual function will
not compile, and this helps catch common errors. The
specifiers serve as documentation; if no specifier is
present, the reader has to check all ancestors of the
class in question to determine if the function or
destructor is virtual or not.</p>

<p>Multiple inheritance is permitted, but multiple <em>implementation</em>
inheritance is strongly discouraged.</p>

<h3 id="Operator_Overloading">Operator Overloading</h3>

<p>Overload operators judiciously. Do not use user-defined literals.</p>

<p class="definition"></p>
<p>C++ permits user code to
<a href="http://en.cppreference.com/w/cpp/language/operators">declare
overloaded versions of the built-in operators</a> using the
<code>operator</code> keyword, so long as one of the parameters
is a user-defined type. The <code>operator</code> keyword also
permits user code to define new kinds of literals using
<code>operator""</code>, and to define type-conversion functions
such as <code>operator bool()</code>.</p>

<p class="pros"></p>
<p>Operator overloading can make code more concise and
intuitive by enabling user-defined types to behave the same
as built-in types. Overloaded operators are the idiomatic names
for certain operations (e.g., <code>==</code>, <code>&lt;</code>,
<code>=</code>, and <code>&lt;&lt;</code>), and adhering to
those conventions can make user-defined types more readable
and enable them to interoperate with libraries that expect
those names.</p>

<p>User-defined literals are a very concise notation for
creating objects of user-defined types.</p>

<p class="cons"></p>
<ul>
  <li>Providing a correct, consistent, and unsurprising
  set of operator overloads requires some care, and failure
  to do so can lead to confusion and bugs.</li>

  <li>Overuse of operators can lead to obfuscated code,
  particularly if the overloaded operator's semantics
  don't follow convention.</li>

  <li>The hazards of function overloading apply just as
  much to operator overloading, if not more so.</li>

  <li>Operator overloads can fool our intuition into
  thinking that expensive operations are cheap, built-in
  operations.</li>

  <li>Finding the call sites for overloaded operators may
  require a search tool that's aware of C++ syntax, rather
  than e.g., grep.</li>

  <li>If you get the argument type of an overloaded operator
  wrong, you may get a different overload rather than a
  compiler error. For example, <code>foo &lt; bar</code>
  may do one thing, while <code>&amp;foo &lt; &amp;bar</code>
  does something totally different.</li>

  <li>Certain operator overloads are inherently hazardous.
  Overloading unary <code>&amp;</code> can cause the same
  code to have different meanings depending on whether
  the overload declaration is visible. Overloads of
  <code>&amp;&amp;</code>, <code>||</code>, and <code>,</code>
  (comma) cannot match the evaluation-order semantics of the
  built-in operators.</li>

  <li>Operators are often defined outside the class,
  so there's a risk of different files introducing
  different definitions of the same operator. If both
  definitions are linked into the same binary, this results
  in undefined behavior, which can manifest as subtle
  run-time bugs.</li>

  <li>User-defined literals (UDLs) allow the creation of new
  syntactic forms that are unfamiliar even to experienced C++
  programmers, such as <code>"Hello World"sv</code> as a
  shorthand for <code>std::string_view("Hello World")</code>.
  Existing notations are clearer, though less terse.</li>

  <li>Because they can't be namespace-qualified, uses of UDLs also require
  use of either using-directives (which <a href="#Namespaces">we ban</a>) or
  using-declarations (which <a href="#Aliases">we ban in header files</a> except
  when the imported names are part of the interface exposed by the header
  file in question).  Given that header files would have to avoid UDL
  suffixes, we prefer to avoid having conventions for literals differ
  between header files and source files.
  </li>
</ul>

<p class="decision"></p>
<p>Define overloaded operators only if their meaning is
obvious, unsurprising, and consistent with the corresponding
built-in operators. For example, use <code>|</code> as a
bitwise- or logical-or, not as a shell-style pipe.</p>

<p>Define operators only on your own types. More precisely,
define them in the same headers, .cc files, and namespaces
as the types they operate on. That way, the operators are available
wherever the type is, minimizing the risk of multiple
definitions. If possible, avoid defining operators as templates,
because they must satisfy this rule for any possible template
arguments. If you define an operator, also define
any related operators that make sense, and make sure they
are defined consistently. For example, if you overload
<code>&lt;</code>, overload all the comparison operators,
and make sure <code>&lt;</code> and <code>&gt;</code> never
return true for the same arguments.</p>

<p>Prefer to define non-modifying binary operators as
non-member functions. If a binary operator is defined as a
class member, implicit conversions will apply to the
right-hand argument, but not the left-hand one. It will
confuse your users if <code>a &lt; b</code> compiles but
<code>b &lt; a</code> doesn't.</p>

<p>Don't go out of your way to avoid defining operator
overloads. For example, prefer to define <code>==</code>,
<code>=</code>, and <code>&lt;&lt;</code>, rather than
<code>Equals()</code>, <code>CopyFrom()</code>, and
<code>PrintTo()</code>. Conversely, don't define
operator overloads just because other libraries expect
them. For example, if your type doesn't have a natural
ordering, but you want to store it in a <code>std::set</code>,
use a custom comparator rather than overloading
<code>&lt;</code>.</p>

<p>Do not overload <code>&amp;&amp;</code>, <code>||</code>,
<code>,</code> (comma), or unary <code>&amp;</code>. Do not overload
<code>operator""</code>, i.e., do not introduce user-defined
literals.  Do not use any such literals provided by others
(including the standard library).</p>

<p>Type conversion operators are covered in the section on
<a href="#Implicit_Conversions">implicit conversions</a>.
The <code>=</code> operator is covered in the section on
<a href="#Copy_Constructors">copy constructors</a>. Overloading
<code>&lt;&lt;</code> for use with streams is covered in the
section on <a href="#Streams">streams</a>. See also the rules on
<a href="#Function_Overloading">function overloading</a>, which
apply to operator overloading as well.</p>

<h3 id="Access_Control">Access Control</h3>

<p>Make classes' data members <code>private</code>, unless they are
<a href="#Constant_Names">constants</a>. This simplifies reasoning about invariants, at the cost
of some easy boilerplate in the form of accessors (usually <code>const</code>) if necessary.</p>

<p>For technical
reasons, we allow data members of a test fixture class defined in a .cc file to
be <code>protected</code> when using


<a href="https://github.com/google/googletest">Google
Test</a>).
If a test fixture class is defined outside of the .cc file it is used in, for example in a .h file,
make data members <code>private</code>.</p>

<h3 id="Declaration_Order">Declaration Order</h3>

<p>Group similar declarations together, placing public parts
earlier.</p>

<p>A class definition should usually start with a
<code>public:</code> section, followed by
<code>protected:</code>, then <code>private:</code>.  Omit
sections that would be empty.</p>

<p>Within each section, generally prefer grouping similar
kinds of declarations together, and generally prefer the
following order: types (including <code>typedef</code>,
<code>using</code>, and nested structs and classes),
constants, factory functions, constructors and assignment
operators, destructor, all other methods, data members.</p>

<p>Do not put large method definitions inline in the
class definition. Usually, only trivial or
performance-critical, and very short, methods may be
defined inline. See <a href="#Inline_Functions">Inline
Functions</a> for more details.</p>

<h2 id="Functions">Functions</h2>

<a id="Function_Parameter_Ordering"></a>
<a id="Output_Parameters"></a>
<h3 id="Inputs_and_Outputs">Inputs and Outputs</h3>

<p>The output of a C++ function is naturally provided via
a return value and sometimes via output parameters (or in/out parameters).</p>

<p>Prefer using return values over output parameters: they
improve readability, and often provide the same or better
performance.</p>

<p>Parameters are either input to the function, output from the
function, or both. Input parameters should usually be values
or <code>const</code> references,
while required (non-nullable) output and input/output parameters should
usually be references. Generally, use <code>absl::optional</code> to represent
optional inputs, and non-<code>const</code> pointers to represent
optional outputs.</p>

<p>
Avoid defining functions that require a <code>const</code> reference parameter
to outlive the call, because <code>const</code> reference parameters bind
to temporaries. Instead, find a way to eliminate the lifetime requirement
(for example, by copying the parameter), or pass it by <code>const</code>
pointer and document the non-null requirement.

</p>

<p>When ordering function parameters, put all input-only
parameters before any output parameters. In particular,
do not add new parameters to the end of the function just
because they are new; place new input-only parameters before
the output parameters. This is not a hard-and-fast rule. Parameters that
are both input and output muddy the waters, and, as always,
consistency with related functions may require you to bend the rule.
Variadic functions may also require unusual parameter ordering.</p>

<h3 id="Write_Short_Functions">Write Short Functions</h3>

<p>Prefer small and focused functions.</p>

<p>We recognize that long functions are sometimes
appropriate, so no hard limit is placed on functions
length. If a function exceeds about 40 lines, think about
whether it can be broken up without harming the structure
of the program.</p>

<p>Even if your long function works perfectly now,
someone modifying it in a few months may add new
behavior. This could result in bugs that are hard to
find. Keeping your functions short and simple makes it
easier for other people to read and modify your code.
Small functions are also easier to test.</p>

<p>You could find long and complicated functions when
working with
some code. Do not be
intimidated by modifying existing code: if working with
such a function proves to be difficult, you find that
errors are hard to debug, or you want to use a piece of
it in several different contexts, consider breaking up
the function into smaller and more manageable pieces.</p>

<h3 id="Function_Overloading">Function Overloading</h3>

<p>Use overloaded functions (including constructors) only if a
reader looking at a call site can get a good idea of what
is happening without having to first figure out exactly
which overload is being called.</p>

<p class="definition"></p>
<p>You may write a function that takes a <code>const
std::string&amp;</code> and overload it with another that
takes <code>const char*</code>. However, in this case consider
std::string_view
 instead.</p>

<pre>class MyClass {
 public:
  void Analyze(const std::string &amp;text);
  void Analyze(const char *text, size_t textlen);
};
</pre>

<p class="pros"></p>
<p>Overloading can make code more intuitive by allowing an
identically-named function to take different arguments.
It may be necessary for templatized code, and it can be
convenient for Visitors.</p>
<p>Overloading based on const or ref qualification may make utility
  code more usable, more efficient, or both.
  (See <a href="http://abseil.io/tips/148">TotW 148</a> for more.)
</p>

<p class="cons"></p>
<p>If a function is overloaded by the argument types alone,
a reader may have to understand C++'s complex matching
rules in order to tell what's going on. Also many people
are confused by the semantics of inheritance if a derived
class overrides only some of the variants of a
function.</p>

<p class="decision"></p>
<p>You may overload a function when there are no semantic differences
between variants. These overloads may vary in types, qualifiers, or
argument count. However, a reader of such a call must not need to know
which member of the overload set is chosen, only that <b>something</b>
from the set is being called. If you can document all entries in the
overload set with a single comment in the header, that is a good sign
that it is a well-designed overload set.</p>

<h3 id="Default_Arguments">Default Arguments</h3>

<p>Default arguments are allowed on non-virtual functions
when the default is guaranteed to always have the same
value. Follow the same restrictions as for <a href="#Function_Overloading">function overloading</a>, and
prefer overloaded functions if the readability gained with
default arguments doesn't outweigh the downsides below.</p>

<p class="pros"></p>
<p>Often you have a function that uses default values, but
occasionally you want to override the defaults. Default
parameters allow an easy way to do this without having to
define many functions for the rare exceptions. Compared
to overloading the function, default arguments have a
cleaner syntax, with less boilerplate and a clearer
distinction between 'required' and 'optional'
arguments.</p>

<p class="cons"></p>
<p>Defaulted arguments are another way to achieve the
semantics of overloaded functions, so all the <a href="#Function_Overloading">reasons not to overload
functions</a> apply.</p>

<p>The defaults for arguments in a virtual function call are
determined by the static type of the target object, and
there's no guarantee that all overrides of a given function
declare the same defaults.</p>

<p>Default parameters are re-evaluated at each call site,
which can bloat the generated code. Readers may also expect
the default's value to be fixed at the declaration instead
of varying at each call.</p>

<p>Function pointers are confusing in the presence of
default arguments, since the function signature often
doesn't match the call signature. Adding
function overloads avoids these problems.</p>

<p class="decision"></p>
<p>Default arguments are banned on virtual functions, where
they don't work properly, and in cases where the specified
default might not evaluate to the same value depending on
when it was evaluated. (For example, don't write <code>void
f(int n = counter++);</code>.)</p>

<p>In some other cases, default arguments can improve the
readability of their function declarations enough to
overcome the downsides above, so they are allowed. When in
doubt, use overloads.</p>

<h3 id="cpplint">cpplint</h3>

<p>Use <code>cpplint.py</code> to detect style errors.</p>

<p><code>cpplint.py</code>
is a tool that reads a source file and identifies many
style errors. It is not perfect, and has both false
positives and false negatives, but it is still a valuable
tool. False positives can be ignored by putting <code>//
NOLINT</code> at the end of the line or
<code>// NOLINTNEXTLINE</code> in the previous line.</p>



<div>
<p>Some projects have instructions on
how to run <code>cpplint.py</code> from their project
tools. If the project you are contributing to does not,
you can download
<a href="https://raw.githubusercontent.com/google/styleguide/gh-pages/cpplint/cpplint.py">
<code>cpplint.py</code></a> separately.</p>
</div>



<h2 id="Other_C++_Features">Other C++ Features</h2>

<h3 id="Friends">Friends</h3>

<p>We allow use of <code>friend</code> classes and functions,
within reason.</p>

<p>Friends should usually be defined in the same file so
that the reader does not have to look in another file to
find uses of the private members of a class. A common use
of <code>friend</code> is to have a
<code>FooBuilder</code> class be a friend of
<code>Foo</code> so that it can construct the inner state
of <code>Foo</code> correctly, without exposing this
state to the world. In some cases it may be useful to
make a unittest class a friend of the class it tests.</p>

<p>Friends extend, but do not break, the encapsulation
boundary of a class. In some cases this is better than
making a member public when you want to give only one
other class access to it. However, most classes should
interact with other classes solely through their public
members.</p>

<h3 id="Exceptions">Exceptions</h3>

<p>We do not use C++ exceptions.</p>

<p class="pros"></p>
<ul>
  <li>Exceptions allow higher levels of an application to
  decide how to handle "can't happen" failures in deeply
  nested functions, without the obscuring and error-prone
  bookkeeping of error codes.</li>



  <div>
  <li>Exceptions are used by most other
  modern languages. Using them in C++ would make it more
  consistent with Python, Java, and the C++ that others
  are familiar with.</li>
  </div>

  <li>Some third-party C++ libraries use exceptions, and
  turning them off internally makes it harder to
  integrate with those libraries.</li>

  <li>Exceptions are the only way for a constructor to
  fail. We can simulate this with a factory function or
  an <code>Init()</code> method, but these require heap
  allocation or a new "invalid" state, respectively.</li>

  <li>Exceptions are really handy in testing
  frameworks.</li>
</ul>

<p class="cons"></p>
<ul>
  <li>When you add a <code>throw</code> statement to an
  existing function, you must examine all of its
  transitive callers. Either they must make at least the
  basic exception safety guarantee, or they must never
  catch the exception and be happy with the program
  terminating as a result. For instance, if
  <code>f()</code> calls <code>g()</code> calls
  <code>h()</code>, and <code>h</code> throws an
  exception that <code>f</code> catches, <code>g</code>
  has to be careful or it may not clean up properly.</li>

  <li>More generally, exceptions make the control flow of
  programs difficult to evaluate by looking at code:
  functions may return in places you don't expect. This
  causes maintainability and debugging difficulties. You
  can minimize this cost via some rules on how and where
  exceptions can be used, but at the cost of more that a
  developer needs to know and understand.</li>

  <li>Exception safety requires both RAII and different
  coding practices. Lots of supporting machinery is
  needed to make writing correct exception-safe code
  easy. Further, to avoid requiring readers to understand
  the entire call graph, exception-safe code must isolate
  logic that writes to persistent state into a "commit"
  phase. This will have both benefits and costs (perhaps
  where you're forced to obfuscate code to isolate the
  commit). Allowing exceptions would force us to always
  pay those costs even when they're not worth it.</li>

  <li>Turning on exceptions adds data to each binary
  produced, increasing compile time (probably slightly)
  and possibly increasing address space pressure.
  </li>

  <li>The availability of exceptions may encourage
  developers to throw them when they are not appropriate
  or recover from them when it's not safe to do so. For
  example, invalid user input should not cause exceptions
  to be thrown. We would need to make the style guide
  even longer to document these restrictions!</li>
</ul>

<p class="decision"></p>
<p>On their face, the benefits of using exceptions
outweigh the costs, especially in new projects. However,
for existing code, the introduction of exceptions has
implications on all dependent code. If exceptions can be
propagated beyond a new project, it also becomes
problematic to integrate the new project into existing
exception-free code. Because most existing C++ code at
Google is not prepared to deal with exceptions, it is
comparatively difficult to adopt new code that generates
exceptions.</p>

<p>Given that Google's existing code is not
exception-tolerant, the costs of using exceptions are
somewhat greater than the costs in a new project. The
conversion process would be slow and error-prone. We
don't believe that the available alternatives to
exceptions, such as error codes and assertions, introduce
a significant burden. </p>

<p>Our advice against using exceptions is not predicated
on philosophical or moral grounds, but practical ones.
 Because we'd like to use our open-source
projects at Google and it's difficult to do so if those
projects use exceptions, we need to advise against
exceptions in Google open-source projects as well.
Things would probably be different if we had to do it all
over again from scratch.</p>

<p>This prohibition also applies to the exception handling related
features added in C++11, such as
<code>std::exception_ptr</code> and
<code>std::nested_exception</code>.</p>

<p>There is an <a href="#Windows_Code">exception</a> to
this rule (no pun intended) for Windows code.</p>

<h3 id="noexcept"><code>noexcept</code></h3>

<p>Specify <code>noexcept</code> when it is useful and correct.</p>

<p class="definition"></p>
<p>The <code>noexcept</code> specifier is used to specify whether
a function will throw exceptions or not. If an exception
escapes from a function marked <code>noexcept</code>, the program
crashes via <code>std::terminate</code>.</p>

<p>The <code>noexcept</code> operator performs a compile-time
check that returns true if an expression is declared to not
throw any exceptions.</p>

<p class="pros"></p>
<ul>
  <li>Specifying move constructors as <code>noexcept</code>
  improves performance in some cases, e.g.,
  <code>std::vector&lt;T&gt;::resize()</code> moves rather than
  copies the objects if T's move constructor is
  <code>noexcept</code>.</li>

  <li>Specifying <code>noexcept</code> on a function can
  trigger compiler optimizations in environments where
  exceptions are enabled, e.g., compiler does not have to
  generate extra code for stack-unwinding, if it knows
  that no exceptions can be thrown due to a
  <code>noexcept</code> specifier.</li>
</ul>

<p class="cons"></p>
<ul>
  <li>

  In projects following this guide
  that have exceptions disabled it is hard
  to ensure that <code>noexcept</code>
  specifiers are correct, and hard to define what
  correctness even means.</li>

  <li>It's hard, if not impossible, to undo <code>noexcept</code>
  because it eliminates a guarantee that callers may be relying
  on, in ways that are hard to detect.</li>
</ul>

<p class="decision"></p>
<p>You may use <code>noexcept</code> when it is useful for
performance if it accurately reflects the intended semantics
of your function, i.e., that if an exception is somehow thrown
from within the function body then it represents a fatal error.
You can assume that <code>noexcept</code> on move constructors
has a meaningful performance benefit. If you think
there is significant performance benefit from specifying
<code>noexcept</code> on some other function, please discuss it
with
your project leads.</p>

<p>Prefer unconditional <code>noexcept</code> if exceptions are
completely disabled (i.e., most Google C++ environments).
Otherwise, use conditional <code>noexcept</code> specifiers
with simple conditions, in ways that evaluate false only in
the few cases where the function could potentially throw.
The tests might include type traits check on whether the
involved operation might throw (e.g.,
<code>std::is_nothrow_move_constructible</code> for
move-constructing objects), or on whether allocation can throw
(e.g., <code>absl::default_allocator_is_nothrow</code> for
standard default allocation). Note in many cases the only
possible cause for an exception is allocation failure (we
believe move constructors should not throw except due to
allocation failure), and there are many applications where it’s
appropriate to treat memory exhaustion as a fatal error rather
than an exceptional condition that your program should attempt
to recover from.  Even for other
potential failures you should prioritize interface simplicity
over supporting all possible exception throwing scenarios:
instead of writing a complicated <code>noexcept</code> clause
that depends on whether a hash function can throw, for example,
simply document that your component doesn’t support hash
functions throwing and make it unconditionally
<code>noexcept</code>.</p>

<h3 id="Run-Time_Type_Information__RTTI_">Run-Time Type
Information (RTTI)</h3>

<p>Avoid using Run Time Type Information (RTTI).</p>

<p class="definition"></p>
<p> RTTI allows a
programmer to query the C++ class of an object at run
time. This is done by use of <code>typeid</code> or
<code>dynamic_cast</code>.</p>

<p class="pros"></p>
<p>The standard alternatives to RTTI (described below)
require modification or redesign of the class hierarchy
in question. Sometimes such modifications are infeasible
or undesirable, particularly in widely-used or mature
code.</p>

<p>RTTI can be useful in some unit tests. For example, it
is useful in tests of factory classes where the test has
to verify that a newly created object has the expected
dynamic type. It is also useful in managing the
relationship between objects and their mocks.</p>

<p>RTTI is useful when considering multiple abstract
objects. Consider</p>

<pre>bool Base::Equal(Base* other) = 0;
bool Derived::Equal(Base* other) {
  Derived* that = dynamic_cast&lt;Derived*&gt;(other);
  if (that == nullptr)
    return false;
  ...
}
</pre>

<p class="cons"></p>
<p>Querying the type of an object at run-time frequently
means a design problem. Needing to know the type of an
object at runtime is often an indication that the design
of your class hierarchy is flawed.</p>

<p>Undisciplined use of RTTI makes code hard to maintain.
It can lead to type-based decision trees or switch
statements scattered throughout the code, all of which
must be examined when making further changes.</p>

<p class="decision"></p>
<p>RTTI has legitimate uses but is prone to abuse, so you
must be careful when using it. You may use it freely in
unittests, but avoid it when possible in other code. In
particular, think twice before using RTTI in new code. If
you find yourself needing to write code that behaves
differently based on the class of an object, consider one
of the following alternatives to querying the type:</p>

<ul>
  <li>Virtual methods are the preferred way of executing
  different code paths depending on a specific subclass
  type. This puts the work within the object itself.</li>

  <li>If the work belongs outside the object and instead
  in some processing code, consider a double-dispatch
  solution, such as the Visitor design pattern. This
  allows a facility outside the object itself to
  determine the type of class using the built-in type
  system.</li>
</ul>

<p>When the logic of a program guarantees that a given
instance of a base class is in fact an instance of a
particular derived class, then a
<code>dynamic_cast</code> may be used freely on the
object.  Usually one
can use a <code>static_cast</code> as an alternative in
such situations.</p>

<p>Decision trees based on type are a strong indication
that your code is on the wrong track.</p>

<pre class="badcode">if (typeid(*data) == typeid(D1)) {
  ...
} else if (typeid(*data) == typeid(D2)) {
  ...
} else if (typeid(*data) == typeid(D3)) {
...
</pre>

<p>Code such as this usually breaks when additional
subclasses are added to the class hierarchy. Moreover,
when properties of a subclass change, it is difficult to
find and modify all the affected code segments.</p>

<p>Do not hand-implement an RTTI-like workaround. The
arguments against RTTI apply just as much to workarounds
like class hierarchies with type tags. Moreover,
workarounds disguise your true intent.</p>

<h3 id="Casting">Casting</h3>

<p>Use C++-style casts
like <code>static_cast&lt;float&gt;(double_value)</code>, or brace
initialization for conversion of arithmetic types like
<code>int64 y = int64{1} &lt;&lt; 42</code>. Do not use
cast formats like <code>(int)x</code> unless the cast is to
<code>void</code>. You may use cast formats like `T(x)` only when
`T` is a class type.</p>

<p class="definition"></p>
<p> C++ introduced a
different cast system from C that distinguishes the types
of cast operations.</p>

<p class="pros"></p>
<p>The problem with C casts is the ambiguity of the operation;
sometimes you are doing a <em>conversion</em>
(e.g., <code>(int)3.5</code>) and sometimes you are doing
a <em>cast</em> (e.g., <code>(int)"hello"</code>). Brace
initialization and C++ casts can often help avoid this
ambiguity. Additionally, C++ casts are more visible when searching for
them.</p>

<p class="cons"></p>
<p>The C++-style cast syntax is verbose and cumbersome.</p>

<p class="decision"></p>
<p>In general, do not use C-style casts. Instead, use these C++-style
casts when explicit type conversion is necessary.
</p>

<ul>
  <li>Use brace initialization to convert arithmetic types
  (e.g., <code>int64{x}</code>).  This is the safest approach because code
  will not compile if conversion can result in information loss.  The
  syntax is also concise.</li>



  <li>Use <code>static_cast</code> as the equivalent of a C-style cast
  that does value conversion, when you need to
  explicitly up-cast a pointer from a class to its superclass, or when
  you need to explicitly cast a pointer from a superclass to a
  subclass.  In this last case, you must be sure your object is
  actually an instance of the subclass.</li>



  <li>Use <code>const_cast</code> to remove the
  <code>const</code> qualifier (see <a href="#Use_of_const">const</a>).</li>

  <li>Use <code>reinterpret_cast</code> to do unsafe conversions of
  pointer types to and from integer and other pointer
  types. Use this
  only if you know what you are doing and you understand the aliasing
  issues. Also, consider the alternative
  <code>absl::bit_cast</code>.</li>

  <li>Use <code>absl::bit_cast</code> to interpret the raw bits of a
  value using a different type of the same size (a type pun), such as
  interpreting the bits of a <code>double</code> as
  <code>int64</code>.</li>
</ul>

<p>See the <a href="#Run-Time_Type_Information__RTTI_">
RTTI section</a> for guidance on the use of
<code>dynamic_cast</code>.</p>

<h3 id="Postincrement_and_Postdecrement">Preincrement and Predecrement</h3>

<p>Use the postfix form (<code>i++</code>) of the increment
and decrement operators unless you need prefix semantics.</p>

<h3 id="Use_of_const">Use of const</h3>

<p>In APIs, use <code>const</code> whenever it makes sense.
<code>constexpr</code> is a better choice for some uses of
const.</p>

<p class="definition"></p>
<p> Declared variables and parameters can be preceded
by the keyword <code>const</code> to indicate the variables
are not changed (e.g., <code>const int foo</code>). Class
functions can have the <code>const</code> qualifier to
indicate the function does not change the state of the
class member variables (e.g., <code>class Foo { int
Bar(char c) const; };</code>).</p>

<p class="pros"></p>
<p>Easier for people to understand how variables are being
used. Allows the compiler to do better type checking,
and, conceivably, generate better code. Helps people
convince themselves of program correctness because they
know the functions they call are limited in how they can
modify your variables. Helps people know what functions
are safe to use without locks in multi-threaded
programs.</p>

<p class="cons"></p>
<p><code>const</code> is viral: if you pass a
<code>const</code> variable to a function, that function
must have <code>const</code> in its prototype (or the
variable will need a <code>const_cast</code>). This can
be a particular problem when calling library
functions.</p>

<p class="decision"></p>
<p>We strongly recommend using <code>const</code>
in APIs (i.e., on function parameters, methods, and
non-local variables) wherever it is meaningful and accurate. This
provides consistent, mostly compiler-verified documentation
of what objects an operation can mutate. Having
a consistent and reliable way to distinguish reads from writes
is critical to writing thread-safe code, and is useful in
many other contexts as well. In particular:</p>

<ul>
  <li>If a function guarantees that it will not modify an argument
  passed by reference or by pointer, the corresponding function parameter
  should be a reference-to-const (<code>const T&amp;</code>) or
  pointer-to-const (<code>const T*</code>), respectively.</li>

  <li>For a function parameter passed by value, <code>const</code> has
  no effect on the caller, thus is not recommended in function
  declarations. See


  <a href="https://abseil.io/tips/109">TotW #109</a>.


  </li><li>Declare methods to be <code>const</code> unless they
  alter the logical state of the object (or enable the user to modify
  that state, e.g., by returning a non-const reference, but that's
  rare), or they can't safely be invoked concurrently.</li>
</ul>

<p>Using <code>const</code> on local variables is neither encouraged
nor discouraged.</p>

<p>All of a class's <code>const</code> operations should be safe
to invoke concurrently with each other. If that's not feasible, the class must
be clearly documented as "thread-unsafe".</p>


<h4>Where to put the const</h4>

<p>Some people favor the form <code>int const *foo</code>
to <code>const int* foo</code>. They argue that this is
more readable because it's more consistent: it keeps the
rule that <code>const</code> always follows the object
it's describing. However, this consistency argument
doesn't apply in codebases with few deeply-nested pointer
expressions since most <code>const</code> expressions
have only one <code>const</code>, and it applies to the
underlying value. In such cases, there's no consistency
to maintain. Putting the <code>const</code> first is
arguably more readable, since it follows English in
putting the "adjective" (<code>const</code>) before the
"noun" (<code>int</code>).</p>

<p>That said, while we encourage putting
<code>const</code> first, we do not require it. But be
consistent with the code around you!</p>

<h3 id="Use_of_constexpr">Use of constexpr</h3>

<p>Use <code>constexpr</code> to define true
constants or to ensure constant initialization.</p>

<p class="definition"></p>
<p> Some variables can be declared <code>constexpr</code>
to indicate the variables are true constants, i.e., fixed at
compilation/link time. Some functions and constructors
can be declared <code>constexpr</code> which enables them
to be used in defining a <code>constexpr</code>
variable.</p>

<p class="pros"></p>
<p>Use of <code>constexpr</code> enables definition of
constants with floating-point expressions rather than
just literals; definition of constants of user-defined
types; and definition of constants with function
calls.</p>

<p class="cons"></p>
<p>Prematurely marking something as constexpr may cause
migration problems if later on it has to be downgraded.
Current restrictions on what is allowed in constexpr
functions and constructors may invite obscure workarounds
in these definitions.</p>

<p class="decision"></p>
<p><code>constexpr</code> definitions enable a more
robust specification of the constant parts of an
interface. Use <code>constexpr</code> to specify true
constants and the functions that support their
definitions. Avoid complexifying function definitions to
enable their use with <code>constexpr</code>. Do not use
<code>constexpr</code> to force inlining.</p>

<h3 id="Integer_Types">Integer Types</h3>

<p>Other than <code>int</code> use types defined in cstdint</p>

<h3 id="Preprocessor_Macros">Preprocessor Macros</h3>

<p>Avoid defining macros, especially in headers; prefer
inline functions, enums, and <code>const</code> variables.
Name macros with a project-specific prefix. Do not use
macros to define pieces of a C++ API.</p>

<p>Macros mean that the code you see is not the same as
the code the compiler sees. This can introduce unexpected
behavior, especially since macros have global scope.</p>

<p>The problems introduced by macros are especially severe
when they are used to define pieces of a C++ API,
and still more so for public APIs. Every error message from
the compiler when developers incorrectly use that interface
now must explain how the macros formed the interface.
Refactoring and analysis tools have a dramatically harder
time updating the interface. As a consequence, we
specifically disallow using macros in this way.
For example, avoid patterns like:</p>

<pre class="badcode">class WOMBAT_TYPE(Foo) {
  // ...

 public:
  EXPAND_PUBLIC_WOMBAT_API(Foo)

  EXPAND_WOMBAT_COMPARISONS(Foo, ==, &lt;)
};
</pre>

<p>Luckily, macros are not nearly as necessary in C++ as
they are in C. Instead of using a macro to inline
performance-critical code, use an inline function.
Instead of using a macro to store a constant, use a
<code>const</code> variable. Instead of using a macro to
"abbreviate" a long variable name, use a reference.
Instead of using a macro to conditionally compile code
... well, don't do that at all (except, of course, for
the <code>#define</code> guards to prevent double
inclusion of header files). It makes testing much more
difficult.</p>

<p>Macros can do things these other techniques cannot,
and you do see them in the codebase, especially in the
lower-level libraries. And some of their special features
(like stringifying, concatenation, and so forth) are not
available through the language proper. But before using a
macro, consider carefully whether there's a non-macro way
to achieve the same result. If you need to use a macro to
define an interface, contact
your project leads to request
a waiver of this rule.</p>

<p>The following usage pattern will avoid many problems
with macros; if you use macros, follow it whenever
possible:</p>

<ul>
  <li>Don't define macros in a <code>.h</code> file.</li>

  <li><code>#define</code> macros right before you use
  them, and <code>#undef</code> them right after.</li>

  <li>Do not just <code>#undef</code> an existing macro
  before replacing it with your own; instead, pick a name
  that's likely to be unique.</li>

  <li>Try not to use macros that expand to unbalanced C++
  constructs, or at least document that behavior
  well.</li>

  <li>Prefer not using <code>##</code> to generate
  function/class/variable names.</li>
</ul>

<p>Exporting macros from headers (i.e., defining them in a header
without <code>#undef</code>ing them before the end of the header)
is extremely strongly discouraged. If you do export a macro from a
header, it must have a globally unique name. To achieve this, it
must be named with a prefix consisting of your project's namespace
name (but upper case). </p>

<h3 id="0_and_nullptr/NULL">0 and nullptr/NULL</h3>

<p>Use <code>nullptr</code> for pointers, and <code>'\0'</code> for chars (and
not the <code>0</code> literal).</p>

<p>For pointers (address values), use <code>nullptr</code>, as this
provides type-safety.</p>

<p>For C++03 projects, prefer <code>NULL</code> to <code>0</code>. While the
values are equivalent, <code>NULL</code> looks more like a pointer to the
reader, and some C++ compilers provide special definitions of <code>NULL</code>
which enable them to give useful warnings. Never use <code>NULL</code> for
numeric (integer or floating-point) values.</p>

<p>Use <code>'\0'</code> for the null character. Using the correct type makes
the code more readable.</p>

<h3 id="sizeof">sizeof</h3>

<p>Prefer <code>sizeof(<var>varname</var>)</code> to
<code>sizeof(<var>type</var>)</code>.</p>

<p>Use <code>sizeof(<var>varname</var>)</code> when you
take the size of a particular variable.
<code>sizeof(<var>varname</var>)</code> will update
appropriately if someone changes the variable type either
now or later. You may use
<code>sizeof(<var>type</var>)</code> for code unrelated
to any particular variable, such as code that manages an
external or internal data format where a variable of an
appropriate C++ type is not convenient.</p>

<pre>MyStruct data;
memset(&amp;data, 0, sizeof(data));
</pre>

<pre class="badcode">memset(&amp;data, 0, sizeof(MyStruct));
</pre>

<pre>if (raw_size &lt; sizeof(int)) {
  LOG(ERROR) &lt;&lt; "compressed record not big enough for count: " &lt;&lt; raw_size;
  return false;
}
</pre>

<h3 id="Lambda_expressions">Lambda expressions</h3>

<p>Use lambda expressions where appropriate. Prefer explicit captures
when the lambda will escape the current scope.</p>

<p class="definition"></p>
<p> Lambda expressions are a concise way of creating anonymous
function objects. They're often useful when passing
functions as arguments. For example:</p>

<pre>std::sort(v.begin(), v.end(), [](int x, int y) {
  return Weight(x) &lt; Weight(y);
});
</pre>

<p> They further allow capturing variables from the enclosing scope either
explicitly by name, or implicitly using a default capture. Explicit captures
require each variable to be listed, as
either a value or reference capture:</p>

<pre>int weight = 3;
int sum = 0;
// Captures `weight` by value and `sum` by reference.
std::for_each(v.begin(), v.end(), [weight, &amp;sum](int x) {
  sum += weight * x;
});
</pre>


<p>Default captures implicitly capture any variable referenced in the
lambda body, including <code>this</code> if any members are used:</p>

<pre>const std::vector&lt;int&gt; lookup_table = ...;
std::vector&lt;int&gt; indices = ...;
// Captures `lookup_table` by reference, sorts `indices` by the value
// of the associated element in `lookup_table`.
std::sort(indices.begin(), indices.end(), [&amp;](int a, int b) {
  return lookup_table[a] &lt; lookup_table[b];
});
</pre>

<p>A variable capture can also have an explicit initializer, which can
  be used for capturing move-only variables by value, or for other situations
  not handled by ordinary reference or value captures:
  </p><pre>std::unique_ptr&lt;Foo&gt; foo = ...;
[foo = std::move(foo)] () {
  ...
}</pre>
  Such captures (often called "init captures" or "generalized lambda captures")
  need not actually "capture" anything from the enclosing scope, or even have
  a name from the enclosing scope; this syntax is a fully general way to define
  members of a lambda object:
  <pre class="neutralcode">[foo = std::vector&lt;int&gt;({1, 2, 3})] () {
  ...
}</pre>
  The type of a capture with an initializer is deduced using the same rules
  as <code>auto</code>.

<p class="pros"></p>
<ul>
  <li>Lambdas are much more concise than other ways of
   defining function objects to be passed to STL
   algorithms, which can be a readability
   improvement.</li>

  <li>Appropriate use of default captures can remove
    redundancy and highlight important exceptions from
    the default.</li>

   <li>Lambdas, <code>std::function</code>, and
   <code>std::bind</code> can be used in combination as a
   general purpose callback mechanism; they make it easy
   to write functions that take bound functions as
   arguments.</li>
</ul>

<p class="cons"></p>
<ul>
  <li>Variable capture in lambdas can be a source of dangling-pointer
  bugs, particularly if a lambda escapes the current scope.</li>

  <li>Default captures by value can be misleading because they do not prevent
  dangling-pointer bugs. Capturing a pointer by value doesn't cause a deep
  copy, so it often has the same lifetime issues as capture by reference.
  This is especially confusing when capturing 'this' by value, since the use
  of 'this' is often implicit.</li>

  <li>Captures actually declare new variables (whether or not the captures have
    initializers), but they look nothing like any other variable declaration
    syntax in C++. In particular, there's no place for the variable's type,
    or even an <code>auto</code> placeholder (although init captures can
    indicate it indirectly, e.g., with a cast). This can make it difficult to
    even recognize them as declarations.</li>

  <li>Init captures inherently rely on <a href="#Type_deduction">type
      deduction</a>, and suffer from many of the same drawbacks as
    <code>auto</code>, with the additional problem that the syntax doesn't
    even cue the reader that deduction is taking place.</li>

  <li>It's possible for use of lambdas to get out of
  hand; very long nested anonymous functions can make
  code harder to understand.</li>

</ul>

<p class="decision"></p>
<ul>
<li>Use lambda expressions where appropriate, with formatting as
described <a href="#Formatting_Lambda_Expressions">below</a>.</li>
<li>Prefer explicit captures if the lambda may escape the current scope.
For example, instead of:
<pre class="badcode">{
  Foo foo;
  ...
  executor-&gt;Schedule([&amp;] { Frobnicate(foo); })
  ...
}
// BAD! The fact that the lambda makes use of a reference to `foo` and
// possibly `this` (if `Frobnicate` is a member function) may not be
// apparent on a cursory inspection. If the lambda is invoked after
// the function returns, that would be bad, because both `foo`
// and the enclosing object could have been destroyed.
</pre>
prefer to write:
<pre>{
  Foo foo;
  ...
  executor-&gt;Schedule([&amp;foo] { Frobnicate(foo); })
  ...
}
// BETTER - The compile will fail if `Frobnicate` is a member
// function, and it's clearer that `foo` is dangerously captured by
// reference.
</pre>
</li>
<li>Use default capture by reference ([&amp;]) only when the
lifetime of the lambda is obviously shorter than any potential
captures.
</li>
<li>Use default capture by value ([=]) only as a means of binding a
few variables for a short lambda, where the set of captured
variables is obvious at a glance. Prefer not to write long or
complex lambdas with default capture by value.
</li>
<li>Use captures only to actually capture variables from the enclosing scope.
  Do not use captures with initializers to introduce new names, or
  to substantially change the meaning of an existing name. Instead,
  declare a new variable in the conventional way and then capture it,
  or avoid the lambda shorthand and define a function object explicitly.</li>
<li>See the section on <a href="#Type_deduction">type deduction</a>
  for guidance on specifying the parameter and return types.</li>

</ul>

<h2 id="Naming">Naming</h2>

<p>The most important consistency rules are those that govern
naming. The style of a name immediately informs us what sort of
thing the named entity is: a type, a variable, a function, a
constant, a macro, etc., without requiring us to search for the
declaration of that entity. The pattern-matching engine in our
brains relies a great deal on these naming rules.
</p>

<p>Naming rules are pretty arbitrary, but
 we feel that
consistency is more important than individual preferences in this
area, so regardless of whether you find them sensible or not,
the rules are the rules.</p>

<h3 id="General_Naming_Rules">General Naming Rules</h3>

<p>Optimize for readability using names that would be clear
even to people on a different team.</p>

<p>Use names that describe the purpose or intent of the object.
Do not worry about saving horizontal space as it is far
more important to make your code immediately
understandable by a new reader. Minimize the use of
abbreviations that would likely be unknown to someone outside
your project (especially acronyms and initialisms). Do not
abbreviate by deleting letters within a word. As a rule of thumb,
an abbreviation is probably OK if it's listed in
 Wikipedia. Generally speaking, descriptiveness should be
proportional to the name's scope of visibility. For example,
<code>n</code> may be a fine name within a 5-line function,
but within the scope of a class, it's likely too vague.</p>

<pre>class MyClass {
 public:
  int CountFooErrors(const std::vector&lt;Foo&gt;&amp; foos) {
    int n = 0;  // Clear meaning given limited scope and context
    for (const auto&amp; foo : foos) {
      ...
      ++n;
    }
    return n;
  }
  void DoSomethingImportant() {
    std::string fqdn = ...;  // Well-known abbreviation for Fully Qualified Domain Name
  }
 private:
  const int kMaxAllowedConnections = ...;  // Clear meaning within context
};
</pre>

<pre class="badcode">class MyClass {
 public:
  int CountFooErrors(const std::vector&lt;Foo&gt;&amp; foos) {
    int total_number_of_foo_errors = 0;  // Overly verbose given limited scope and context
    for (int foo_index = 0; foo_index &lt; foos.size(); ++foo_index) {  // Use idiomatic `i`
      ...
      ++total_number_of_foo_errors;
    }
    return total_number_of_foo_errors;
  }
  void DoSomethingImportant() {
    int cstmr_id = ...;  // Deletes internal letters
  }
 private:
  const int kNum = ...;  // Unclear meaning within broad scope
};
</pre>

<p>Note that certain universally-known abbreviations are OK, such as
<code>i</code> for an iteration variable and <code>T</code> for a
template parameter.</p>

<p>For the purposes of the naming rules below, a "word" is anything that you
would write in English without internal spaces. This includes abbreviations,
such as acronyms and initialisms. For names written in mixed case (also
sometimes referred to as
"<a href="https://en.wikipedia.org/wiki/Camel_case">camel case</a>" or
"<a href="https://en.wiktionary.org/wiki/Pascal_case">Pascal case</a>"), in
which the first letter of each word is capitalized, prefer to capitalize
abbreviations as single words, e.g., <code>StartRpc()</code> rather than
<code>StartRPC()</code>.</p>

<p>Template parameters should follow the naming style for their
category: type template parameters should follow the rules for
<a href="#Type_Names">type names</a>, and non-type template
parameters should follow the rules for <a href="#Variable_Names">
variable names</a>.

</p><h3 id="File_Names">File Names</h3>

<p>Filenames should be all uppercamelcase and cannot include
underscores (<code>_</code>) or dashes (<code>-</code>).
Follow the convention that your

<h3 id="Type_Names">Type Names</h3>

<p>Type names start with a capital letter and have a capital
letter for each new word, with no underscores:
<code>MyExcitingClass</code>, <code>MyExcitingEnum</code>.</p>

<p>The names of all types — classes, structs, type aliases,
enums, and type template parameters — have the same naming convention.
Type names should start with a capital letter and have a capital letter
for each new word. No underscores. For example:</p>

<pre>// classes and structs
class UrlTable { ...
class UrlTableTester { ...
struct UrlTableProperties { ...

// typedefs
typedef hash_map&lt;UrlTableProperties *, std::string&gt; PropertiesMap;

// using aliases
using PropertiesMap = hash_map&lt;UrlTableProperties *, std::string&gt;;

// enums
enum class UrlTableError { ...
</pre>

<h3 id="Variable_Names">Variable Names</h3>

<p>The names of variables (including function parameters) and data members are
all lowercamelcase. Data members of classes (but not
structs) additionally have prefixed "m_". Pointer variables should be prefixed with "p" and reference variables should be prefixed with "r".</p>

<h4>Class Data Members</h4>

<p>Data members of classes, both static and non-static, are
named like ordinary nonmember variables, but with a "m_" as a prefix.</p>

<pre>class TableInfo {
  ...
 private:
  std::string m_tablename;  // OK - underscore at end.
  static Pool&lt;TableInfo&gt;* m_pool;  // OK.
};
</pre>

<h4>Struct Data Members</h4>

<p>Data members of structs, both static and non-static,
are named like ordinary nonmember variables. They do not have
the trailing underscores that data members in classes have.</p>

<pre>struct UrlTableProperties {
  std::string name;
  int num_entries;
  static Pool&lt;UrlTableProperties&gt;* pool;
};
</pre>


<p>See <a href="#Structs_vs._Classes">Structs vs.
Classes</a> for a discussion of when to use a struct
versus a class.</p>

<h3 id="Constant_Names">Constant Names</h3>

<p>Constant names use CONSTANT_CASE: all uppercase letters, with each word separated from the next by a single underscore.</p>

<pre>const int DAYS_IN_A_WEEK = 7;</pre>

<h3 id="Function_Names">Function Names</h3>

<p>Regular functions have mixed case; accessors and mutators may be named
like variables.</p>

<p>Ordinarily, functions should start with a capital letter and have a
capital letter for each new word.</p>

<pre>AddTableEntry()
DeleteUrl()
OpenFileOrDie()
</pre>

<p>(The same naming rule applies to class- and namespace-scope
constants that are exposed as part of an API and that are intended to look
like functions, because the fact that they're objects rather than functions
is an unimportant implementation detail.)</p>

<p>Accessors and mutators (get and set functions) may be named like
variables. These often correspond to actual member variables, but this is
not required. For example, <code>int count()</code> and <code>void
set_count(int count)</code>.</p>

<h3 id="Namespace_Names">Namespace Names</h3>
Namespace names are all uppercamelcase. 

<h3 id="Macro_Names">Macro Names</h3>

<p>You're not really going to <a href="#Preprocessor_Macros">
define a macro</a>, are you? If you do, they're like this:
<code>MY_MACRO_THAT_SCARES_SMALL_CHILDREN_AND_ADULTS_ALIKE</code>.
</p>

<p>Please see the <a href="#Preprocessor_Macros">description
of macros</a>; in general macros should <em>not</em> be used.
However, if they are absolutely needed, then they should be
named with all capitals and underscores.</p>

<pre>#define ROUND(x) ...
#define PI_ROUNDED 3.0
</pre>

<h2 id="Comments">Comments</h2>

<p>Comments are absolutely vital to keeping our code readable. The following rules describe what you
should comment and where. But remember: while comments are very important, the best code is
self-documenting. Giving sensible names to types and variables is much better than using obscure
names that you must then explain through comments.</p>

<p>When writing your comments, write for your audience: the
next
contributor who will need to
understand your code. Be generous — the next
one may be you!</p>

<h3 id="Comment_Style">Comment Style</h3>

<p>Use either the <code>//</code> or <code>/* */</code>
syntax, as long as you are consistent.</p>

<p>You can use either the <code>//</code> or the <code>/*
*/</code> syntax; however, <code>//</code> is
<em>much</em> more common. Be consistent with how you
comment and what style you use where.</p>

<h3 id="Class_Comments">Class Comments</h3>

<p>Every non-obvious class or struct declaration should have an
accompanying comment that describes what it is for and how it should
be used.</p>

<pre>// Iterates over the contents of a GargantuanTable.
// Example:
//    GargantuanTableIterator* iter = table-&gt;NewIterator();
//    for (iter-&gt;Seek("foo"); !iter-&gt;done(); iter-&gt;Next()) {
//      process(iter-&gt;key(), iter-&gt;value());
//    }
//    delete iter;
class GargantuanTableIterator {
  ...
};
</pre>

<p>The class comment should provide the reader with enough information to know
how and when to use the class, as well as any additional considerations
necessary to correctly use the class. Document the synchronization assumptions
the class makes, if any. If an instance of the class can be accessed by
multiple threads, take extra care to document the rules and invariants
surrounding multithreaded use.</p>

<p>The class comment is often a good place for a small example code snippet
demonstrating a simple and focused usage of the class.</p>

<p>When sufficiently separated (e.g., <code>.h</code> and <code>.cc</code>
files), comments describing the use of the class should go together with its
interface definition; comments about the class operation and implementation
should accompany the implementation of the class's methods.</p>

<h3 id="Function_Comments">Function Comments</h3>

<p>Declaration comments describe use of the function (when it is
non-obvious); comments at the definition of a function describe
operation.</p>

<h4>Function Declarations</h4>

<p>Almost every function declaration should have comments immediately
preceding it that describe what the function does and how to use
it. These comments may be omitted only if the function is simple and
obvious (e.g., simple accessors for obvious properties of the
class).  These comments should open with descriptive verbs in the
indicative mood ("Opens the file") rather than verbs in the imperative
("Open the file"). The comment describes the function; it does not
tell the function what to do. In general, these comments do not
describe how the function performs its task. Instead, that should be
left to comments in the function definition.</p>

<p>Types of things to mention in comments at the function
declaration:</p>

<ul>
  <li>What the inputs and outputs are.</li>

  <li>For class member functions: whether the object
  remembers reference arguments beyond the duration of
  the method call, and whether it will free them or
  not.</li>

  <li>If the function allocates memory that the caller
  must free.</li>

  <li>Whether any of the arguments can be a null
  pointer.</li>

  <li>If there are any performance implications of how a
  function is used.</li>

  <li>If the function is re-entrant. What are its
  synchronization assumptions?</li>
 </ul>

<p>Here is an example:</p>

<pre>// Returns an iterator for this table.  It is the client's
// responsibility to delete the iterator when it is done with it,
// and it must not use the iterator once the GargantuanTable object
// on which the iterator was created has been deleted.
//
// The iterator is initially positioned at the beginning of the table.
//
// This method is equivalent to:
//    Iterator* iter = table-&gt;NewIterator();
//    iter-&gt;Seek("");
//    return iter;
// If you are going to immediately seek to another place in the
// returned iterator, it will be faster to use NewIterator()
// and avoid the extra seek.
Iterator* GetIterator() const;
</pre>

<p>However, do not be unnecessarily verbose or state the
completely obvious.</p>

<p>When documenting function overrides, focus on the
specifics of the override itself, rather than repeating
the comment from the overridden function.  In many of these
cases, the override needs no additional documentation and
thus no comment is required.</p>

<p>When commenting constructors and destructors, remember
that the person reading your code knows what constructors
and destructors are for, so comments that just say
something like "destroys this object" are not useful.
Document what constructors do with their arguments (for
example, if they take ownership of pointers), and what
cleanup the destructor does. If this is trivial, just
skip the comment. It is quite common for destructors not
to have a header comment.</p>

<h4>Function Definitions</h4>

<p>If there is anything tricky about how a function does
its job, the function definition should have an
explanatory comment. For example, in the definition
comment you might describe any coding tricks you use,
give an overview of the steps you go through, or explain
why you chose to implement the function in the way you
did rather than using a viable alternative. For instance,
you might mention why it must acquire a lock for the
first half of the function but why it is not needed for
the second half.</p>

<p>Note you should <em>not</em> just repeat the comments
given with the function declaration, in the
<code>.h</code> file or wherever. It's okay to
recapitulate briefly what the function does, but the
focus of the comments should be on how it does it.</p>

<h3 id="Variable_Comments">Variable Comments</h3>

<p>In general the actual name of the variable should be
descriptive enough to give a good idea of what the variable
is used for. In certain cases, more comments are required.</p>

<h4>Class Data Members</h4>

<p>The purpose of each class data member (also called an instance
variable or member variable) must be clear. If there are any
invariants (special values, relationships between members, lifetime
requirements) not clearly expressed by the type and name, they must be
commented. However, if the type and name suffice (<code>int
num_events_;</code>), no comment is needed.</p>

<p>In particular, add comments to describe the existence and meaning
of sentinel values, such as nullptr or -1, when they are not
obvious. For example:</p>

<pre>private:
 // Used to bounds-check table accesses. -1 means
 // that we don't yet know how many entries the table has.
 int num_total_entries_;
</pre>

<h4>Global Variables</h4>

<p>All global variables should have a comment describing what they
are, what they are used for, and (if unclear) why it needs to be
global. For example:</p>

<pre>// The total number of tests cases that we run through in this regression test.
const int kNumTestCases = 6;
</pre>

<h3 id="Implementation_Comments">Implementation Comments</h3>

<p>In your implementation you should have comments in tricky,
non-obvious, interesting, or important parts of your code.</p>

<h4>Explanatory Comments</h4>

<p>Tricky or complicated code blocks should have comments
before them. Example:</p>

<pre>// Divide result by two, taking into account that x
// contains the carry from the add.
for (int i = 0; i &lt; result-&gt;size(); ++i) {
  x = (x &lt;&lt; 8) + (*result)[i];
  (*result)[i] = x &gt;&gt; 1;
  x &amp;= 1;
}
</pre>

<h4>Line-end Comments</h4>

<p><b>DO NOT USE LINE-END COMMENTS</b></p>

<h4 id="Implementation_Comment_Donts">Don'ts</h4>

<p>Do not state the obvious. In particular, don't literally describe what
code does, unless the behavior is nonobvious to a reader who understands
C++ well. Instead, provide higher level comments that describe <i>why</i>
the code does what it does, or make the code self describing.</p>

Compare this:

<pre class="badcode">// Find the element in the vector.  &lt;-- Bad: obvious!
auto iter = std::find(v.begin(), v.end(), element);
if (iter != v.end()) {
  Process(element);
}
</pre>

To this:

<pre>// Process "element" unless it was already processed.
auto iter = std::find(v.begin(), v.end(), element);
if (iter != v.end()) {
  Process(element);
}
</pre>

Self-describing code doesn't need a comment. The comment from
the example above would be obvious:

<pre>if (!IsAlreadyProcessed(element)) {
  Process(element);
}
</pre>

<h3 id="Punctuation,_Spelling_and_Grammar">Punctuation, Spelling, and Grammar</h3>

<p>Pay attention to punctuation, spelling, and grammar; it is
easier to read well-written comments than badly written
ones.</p>

<p>Comments should be as readable as narrative text, with
proper capitalization and punctuation. In many cases,
complete sentences are more readable than sentence
fragments. Shorter comments, such as comments at the end
of a line of code, can sometimes be less formal, but you
should be consistent with your style.</p>

<p>Although it can be frustrating to have a code reviewer
point out that you are using a comma when you should be
using a semicolon, it is very important that source code
maintain a high level of clarity and readability. Proper
punctuation, spelling, and grammar help with that
goal.</p>

<h3 id="TODO_Comments">TODO Comments</h3>

<p>Use <code>TODO</code> comments for code that is temporary,
a short-term solution, or good-enough but not perfect.</p>

<p><code>TODO</code>s should include the string
<code>TODO</code> in all caps, followed by the

name, e-mail address, bug ID, or other
identifier
of the person or issue with the best context
about the problem referenced by the <code>TODO</code>. The
main purpose is to have a consistent <code>TODO</code> that
can be searched to find out how to get more details upon
request. A <code>TODO</code> is not a commitment that the
person referenced will fix the problem. Thus when you create
a <code>TODO</code> with a name, it is almost always your
name that is given.</p>



<div>
<pre>// TODO(kl@gmail.com): Use a "*" here for concatenation operator.
// TODO(Zeke) change this to use relations.
// TODO(bug 12345): remove the "Last visitors" feature.
</pre>
</div>

<p>If your <code>TODO</code> is of the form "At a future
date do something" make sure that you either include a
very specific date ("Fix by November 2005") or a very
specific event ("Remove this code when all clients can
handle XML responses.").</p>

<h2 id="Formatting">Formatting</h2>

<p>Coding style and formatting are pretty arbitrary, but a

project is much easier to follow
if everyone uses the same style. Individuals may not agree with every
aspect of the formatting rules, and some of the rules may take
some getting used to, but it is important that all

project contributors follow the
style rules so that
they can all read and understand
everyone's code easily.</p>



<div>
<p>To help you format code correctly, we've created a
<a href="https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el">
settings file for emacs</a>.</p>
</div>

<h3 id="Line_Length">Line Length</h3>

<p>Each line of text in your code should be at most 80
characters long.</p>



<div>
<p>We recognize that this rule is
controversial, but so much existing code already adheres
to it, and we feel that consistency is important.</p>
</div>

<p class="pros"></p>
<p>Those who favor  this rule
argue that it is rude to force them to resize
their windows and there is no need for anything longer.
Some folks are used to having several code windows
side-by-side, and thus don't have room to widen their
windows in any case. People set up their work environment
assuming a particular maximum window width, and 80
columns has been the traditional standard. Why change
it?</p>

<p class="cons"></p>
<p>Proponents of change argue that a wider line can make
code more readable. The 80-column limit is an hidebound
throwback to 1960s mainframes;  modern equipment has wide screens that
can easily show longer lines.</p>

<p class="decision"></p>
<p> 80 characters is the maximum.</p>

<p>A line may exceed 80 characters if it is</p>

<ul>
  <li>a comment line which is not feasible to split without harming
  readability, ease of cut and paste or auto-linking -- e.g., if a line
  contains an example command or a literal URL longer than 80 characters.</li>

  <li>a raw-string literal with content that exceeds 80 characters.  Except for
  test code, such literals should appear near the top of a file.</li>

  <li>an include statement.</li>

  <li>a <a href="#The__define_Guard">header guard</a></li>

  <li>a using-declaration</li>
</ul>

<h3 id="Non-ASCII_Characters">Non-ASCII Characters</h3>

<p>Non-ASCII characters should be rare, and must use UTF-8
formatting.</p>

<p>You shouldn't hard-code user-facing text in source,
even English, so use of non-ASCII characters should be
rare. However, in certain cases it is appropriate to
include such words in your code. For example, if your
code parses data files from foreign sources, it may be
appropriate to hard-code the non-ASCII string(s) used in
those data files as delimiters. More commonly, unittest
code (which does not  need to be localized) might
contain non-ASCII strings. In such cases, you should use
UTF-8, since that is  an encoding
understood by most tools able to handle more than just
ASCII.</p>

<p>Hex encoding is also OK, and encouraged where it
enhances readability — for example,
<code>"\xEF\xBB\xBF"</code>, or, even more simply,
<code>u8"\uFEFF"</code>, is the Unicode zero-width
no-break space character, which would be invisible if
included in the source as straight UTF-8.</p>

<p>Use the <code>u8</code> prefix
to guarantee that a string literal containing
<code>\uXXXX</code> escape sequences is encoded as UTF-8.
Do not use it for strings containing non-ASCII characters
encoded as UTF-8, because that will produce incorrect
output if the compiler does not interpret the source file
as UTF-8. </p>

<p>You shouldn't use the C++11 <code>char16_t</code> and
<code>char32_t</code> character types, since they're for
non-UTF-8 text. For similar reasons you also shouldn't
use <code>wchar_t</code> (unless you're writing code that
interacts with the Windows API, which uses
<code>wchar_t</code> extensively).</p>

<h3 id="Spaces_vs._Tabs">Tabs</h3>

<p>Use tabs.</p>

<h3 id="Function_Declarations_and_Definitions">Function Declarations and Definitions</h3>

<p>Return type on the same line as function name, parameters
on the same line if they fit. Wrap parameter lists which do
not fit on a single line as you would wrap arguments in a
<a href="#Function_Calls">function call</a>.</p>

<p>Functions look like this:</p>


<pre>ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
  ...
}
</pre>

<p>If you have too much text to fit on one line:</p>

<pre>ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                             Type par_name3) {
  DoSomething();
  ...
}
</pre>

<p>or if you cannot fit even the first parameter:</p>

<pre>ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4 space indent
    Type par_name2,
    Type par_name3) {
  DoSomething();  // 2 space indent
  ...
}
</pre>

<p>Some points to note:</p>

<ul>
  <li>Choose good parameter names.</li>

  <li>A parameter name may be omitted only if the parameter is not used in the
  function's definition.</li>

  <li>If you cannot fit the return type and the function
  name on a single line, break between them.</li>

  <li>If you break after the return type of a function
  declaration or definition, do not indent.</li>

  <li>The open parenthesis is always on the same line as
  the function name.</li>

  <li>There is never a space between the function name
  and the open parenthesis.</li>

  <li>There is never a space between the parentheses and
  the parameters.</li>

  <li>The open curly brace is always on the end of the last line of the function
  declaration, not the start of the next line.</li>

  <li>The close curly brace is either on the last line by
  itself or on the same line as the open curly brace.</li>

  <li>There should be a space between the close
  parenthesis and the open curly brace.</li>

  <li>All parameters should be aligned if possible.</li>

  <li>Default indentation is 2 spaces.</li>

  <li>Wrapped parameters have a 4 space indent.</li>
</ul>

<p>Unused parameters that are obvious from context may be omitted:</p>

<pre>class Foo {
 public:
  Foo(const Foo&amp;) = delete;
  Foo&amp; operator=(const Foo&amp;) = delete;
};
</pre>

<p>Unused parameters that might not be obvious should comment out the variable
name in the function definition:</p>

<pre>class Shape {
 public:
  virtual void Rotate(double radians) = 0;
};

class Circle : public Shape {
 public:
  void Rotate(double radians) override;
};

void Circle::Rotate(double /*radians*/) {}
</pre>

<pre class="badcode">// Bad - if someone wants to implement later, it's not clear what the
// variable means.
void Circle::Rotate(double) {}
</pre>

<p>Attributes, and macros that expand to attributes, appear at the very
beginning of the function declaration or definition, before the
return type:</p>
<pre>ABSL_MUST_USE_RESULT bool IsOk();
</pre>

<h3 id="Formatting_Lambda_Expressions">Lambda Expressions</h3>

<p>Format parameters and bodies as for any other function, and capture
lists like other comma-separated lists.</p>

<p>For by-reference captures, do not leave a space between the
ampersand (&amp;) and the variable name.</p>
<pre>int x = 0;
auto x_plus_n = [&amp;x](int n) -&gt; int { return x + n; }
</pre>
<p>Short lambdas may be written inline as function arguments.</p>
<pre>std::set&lt;int&gt; blacklist = {7, 8, 9};
std::vector&lt;int&gt; digits = {3, 9, 1, 8, 4, 7, 1};
digits.erase(std::remove_if(digits.begin(), digits.end(), [&amp;blacklist](int i) {
               return blacklist.find(i) != blacklist.end();
             }),
             digits.end());
</pre>

<h3 id="Floating_Literals">Floating-point Literals</h3>

<p>Floating-point literals should always have a radix point, with digits on both
sides, even if they use exponential notation. Readability is improved if all
floating-point literals take this familiar form, as this helps ensure that they
are not mistaken for integer literals, and that the
<code>E</code>/<code>e</code> of the exponential notation is not mistaken for a
hexadecimal digit. It is fine to initialize a floating-point variable with an
integer literal (assuming the variable type can exactly represent that integer),
but note that a number in exponential notation is never an integer literal.
</p>

<pre class="badcode">float f = 1.f;
long double ld = -.5L;
double d = 1248e6;
</pre>

<pre class="goodcode">float f = 1.0f;
float f2 = 1;   // Also OK
long double ld = -0.5L;
double d = 1248.0e6;
</pre>


<h3 id="Function_Calls">Function Calls</h3>

<p>Either write the call all on a single line, wrap the
arguments at the parenthesis, or start the arguments on a new
line indented by four spaces and continue at that 4 space
indent. In the absence of other considerations, use the
minimum number of lines, including placing multiple arguments
on each line where appropriate.</p>

<p>Function calls have the following format:</p>
<pre>bool result = DoSomething(argument1, argument2, argument3);
</pre>

<p>If the arguments do not all fit on one line, they
should be broken up onto multiple lines, with each
subsequent line aligned with the first argument. Do not
add spaces after the open paren or before the close
paren:</p>
<pre>bool result = DoSomething(averyveryveryverylongargument1,
                          argument2, argument3);
</pre>

<p>Arguments may optionally all be placed on subsequent
lines with a four space indent:</p>
<pre>if (...) {
  ...
  ...
  if (...) {
    bool result = DoSomething(
        argument1, argument2,  // 4 space indent
        argument3, argument4);
    ...
  }
</pre>

<p>Put multiple arguments on a single line to reduce the
number of lines necessary for calling a function unless
there is a specific readability problem. Some find that
formatting with strictly one argument on each line is
more readable and simplifies editing of the arguments.
However, we prioritize for the reader over the ease of
editing arguments, and most readability problems are
better addressed with the following techniques.</p>

<p>If having multiple arguments in a single line decreases
readability due to the complexity or confusing nature of the
expressions that make up some arguments, try creating
variables that capture those arguments in a descriptive name:</p>
<pre>int my_heuristic = scores[x] * y + bases[x];
bool result = DoSomething(my_heuristic, x, y, z);
</pre>

<p>Or put the confusing argument on its own line with
an explanatory comment:</p>
<pre>bool result = DoSomething(scores[x] * y + bases[x],  // Score heuristic.
                          x, y, z);
</pre>

<p>If there is still a case where one argument is
significantly more readable on its own line, then put it on
its own line. The decision should be specific to the argument
which is made more readable rather than a general policy.</p>

<p>Sometimes arguments form a structure that is important
for readability. In those cases, feel free to format the
arguments according to that structure:</p>
<pre>// Transform the widget by a 3x3 matrix.
my_widget.Transform(x1, x2, x3,
                    y1, y2, y3,
                    z1, z2, z3);
</pre>

<h3 id="Conditionals">Conditionals</h3>

<p>The <code>if</code> and <code>else</code> keywords belong on separate lines.
  There should be a space between the <code>if</code> and the open parenthesis,
  and between the close parenthesis and the curly brace (if any), but no space
  between the parentheses and the condition.</p>

<pre>if (condition) {  // no spaces inside parentheses
  ...  // 2 space indent.
} else if (...) {  // The else goes on the same line as the closing brace.
  ...
} else {
  ...
}
</pre>

<pre class="badcode">if(condition) {   // Bad - space missing after IF.
if ( condition ) { // Bad - space between the parentheses and the condition
if (condition){   // Bad - space missing before {.
if(condition){    // Doubly bad.
</pre>

<pre>if (condition) {  // Good - proper space after IF and before {.
</pre>

<p>Short conditional statements may be written on one
line if this enhances readability. You may use this only
when the line is brief and the statement does not use the
<code>else</code> clause.</p>

<pre>if (x == kFoo) return new Foo();
if (x == kBar) return new Bar();
</pre>

<p>This is not allowed when the if statement has an
<code>else</code>:</p>

<pre class="badcode">// Not allowed - IF statement on one line when there is an ELSE clause
if (x) DoThis();
else DoThat();
</pre>

<p>In general, curly braces are not required for
single-line statements, but they are allowed if you like
them; conditional or loop statements with complex
conditions or statements may be more readable with curly
braces. Some
projects require that an
<code>if</code> must always have an accompanying
brace.</p>

<pre>if (condition)
  DoSomething();  // 2 space indent.

if (condition) {
  DoSomething();  // 2 space indent.
}
</pre>

<p>However, if one part of an
<code>if</code>-<code>else</code> statement uses curly
braces, the other part must too:</p>

<pre class="badcode">// Not allowed - curly on IF but not ELSE
if (condition) {
  foo;
} else
  bar;

// Not allowed - curly on ELSE but not IF
if (condition)
  foo;
else {
  bar;
}
</pre>

<pre>// Curly braces around both IF and ELSE required because
// one of the clauses used braces.
if (condition) {
  foo;
} else {
  bar;
}
</pre>

<h3 id="Loops_and_Switch_Statements">Loops and Switch Statements</h3>

<p>Switch statements may use braces for blocks. Annotate
non-trivial fall-through between cases.
Braces are optional for single-statement loops.
Empty loop bodies should use either empty braces or <code>continue</code>.</p>

<p><code>case</code> blocks in <code>switch</code>
statements can have curly braces or not, depending on
your preference. If you do include curly braces they
should be placed as shown below.</p>

<p>If not conditional on an enumerated value, switch
statements should always have a <code>default</code> case
(in the case of an enumerated value, the compiler will
warn you if any values are not handled). If the default
case should never execute, treat this as an error. For example:

</p>

<div>
<pre>switch (var) {
  case 0: {  // 2 space indent
    ...      // 4 space indent
    break;
  }
  case 1: {
    ...
    break;
  }
  default: {
    assert(false);
  }
}
</pre>
</div>

<p>Fall-through from one case label to
another must be annotated using the
<code>ABSL_FALLTHROUGH_INTENDED;</code> macro (defined in

<code>absl/base/macros.h</code>).
<code>ABSL_FALLTHROUGH_INTENDED;</code> should be placed at a
point of execution where a fall-through to the next case
label occurs. A common exception is consecutive case
labels without intervening code, in which case no
annotation is needed.</p>

<pre>switch (x) {
  case 41:  // No annotation needed here.
  case 43:
    if (dont_be_picky) {
      // Use this instead of or along with annotations in comments.
      ABSL_FALLTHROUGH_INTENDED;
    } else {
      CloseButNoCigar();
      break;
    }
  case 42:
    DoSomethingSpecial();
    ABSL_FALLTHROUGH_INTENDED;
  default:
    DoSomethingGeneric();
    break;
}
</pre>

<p> Braces are optional for single-statement loops.</p>

<pre>for (int i = 0; i &lt; kSomeNumber; ++i)
  printf("I love you\n");

for (int i = 0; i &lt; kSomeNumber; ++i) {
  printf("I take it back\n");
}
</pre>


<p>Empty loop bodies should use either an empty pair of braces or
<code>continue</code> with no braces, rather than a single semicolon.</p>

<pre>while (condition) {
  // Repeat test until it returns false.
}
for (int i = 0; i &lt; kSomeNumber; ++i) {}  // Good - one newline is also OK.
while (condition) continue;  // Good - continue indicates no logic.
</pre>

<pre class="badcode">while (condition);  // Bad - looks like part of do/while loop.
</pre>

<h3 id="Pointer_and_Reference_Expressions">Pointer and Reference Expressions</h3>

<p>No spaces around period or arrow. Pointer operators do not
have trailing spaces.</p>

<p>The following are examples of correctly-formatted
pointer and reference expressions:</p>

<pre>x = *p;
p = &amp;x;
x = r.y;
x = r-&gt;y;
</pre>

<p>Note that:</p>

<ul>
  <li>There are no spaces around the period or arrow when
  accessing a member.</li>

   <li>Pointer operators have no space after the
   <code>*</code> or <code>&amp;</code>.</li>
</ul>

<p>When declaring a pointer variable or argument, you may
place the asterisk adjacent to either the type or to the
variable name:</p>

<pre>// These are fine, space preceding.
char *c;
const std::string &amp;str;

// These are fine, space following.
char* c;
const std::string&amp; str;
</pre>

<p>You should do this consistently within a single
file,
so, when modifying an existing file, use the style in
that file.</p>

It is allowed (if unusual) to declare multiple variables in the same
declaration, but it is disallowed if any of those have pointer or
reference decorations. Such declarations are easily misread.
<pre>// Fine if helpful for readability.
int x, y;
</pre>
<pre class="badcode">int x, *y;  // Disallowed - no &amp; or * in multiple declaration
char * c;  // Bad - spaces on both sides of *
const std::string &amp; str;  // Bad - spaces on both sides of &amp;
</pre>

<h3 id="Boolean_Expressions">Boolean Expressions</h3>

<p>When you have a boolean expression that is longer than the
<a href="#Line_Length">standard line length</a>, be
consistent in how you break up the lines.</p>

<p>In this example, the logical AND operator is always at
the end of the lines:</p>

<pre>if (this_one_thing &gt; this_other_thing &amp;&amp;
    a_third_thing == a_fourth_thing &amp;&amp;
    yet_another &amp;&amp; last_one) {
  ...
}
</pre>

<p>Note that when the code wraps in this example, both of
the <code>&amp;&amp;</code> logical AND operators are at
the end of the line. This is more common in Google code,
though wrapping all operators at the beginning of the
line is also allowed. Feel free to insert extra
parentheses judiciously because they can be very helpful
in increasing readability when used
appropriately, but be careful about overuse. Also note that you
should always use the punctuation operators, such as
<code>&amp;&amp;</code> and <code>~</code>, rather than
the word operators, such as <code>and</code> and
<code>compl</code>.</p>

<h3 id="Return_Values">Return Values</h3>

<p>Do not needlessly surround the <code>return</code>
expression with parentheses.</p>

<p>Use parentheses in <code>return expr;</code> only
where you would use them in <code>x = expr;</code>.</p>

<pre>return result;                  // No parentheses in the simple case.
// Parentheses OK to make a complex expression more readable.
return (some_long_condition &amp;&amp;
        another_condition);
</pre>

<pre class="badcode">return (value);                // You wouldn't write var = (value);
return(result);                // return is not a function!
</pre>



<h3 id="Variable_and_Array_Initialization">Variable and Array Initialization</h3>

<p>Your choice of <code>=</code>, <code>()</code>, or
<code>{}</code>.</p>

<p>You may choose between <code>=</code>,
<code>()</code>, and <code>{}</code>; the following are
all correct:</p>

<pre>int x = 3;
int x(3);
int x{3};
std::string name = "Some Name";
std::string name("Some Name");
std::string name{"Some Name"};
</pre>

<p>Be careful when using a braced initialization list <code>{...}</code>
on a type with an <code>std::initializer_list</code> constructor.
A nonempty <i>braced-init-list</i> prefers the
<code>std::initializer_list</code> constructor whenever
possible. Note that empty braces <code>{}</code> are special, and
will call a default constructor if available. To force the
non-<code>std::initializer_list</code> constructor, use parentheses
instead of braces.</p>

<pre>std::vector&lt;int&gt; v(100, 1);  // A vector containing 100 items: All 1s.
std::vector&lt;int&gt; v{100, 1};  // A vector containing 2 items: 100 and 1.
</pre>

<p>Also, the brace form prevents narrowing of integral
types. This can prevent some types of programming
errors.</p>

<pre>int pi(3.14);  // OK -- pi == 3.
int pi{3.14};  // Compile error: narrowing conversion.
</pre>

<h3 id="Preprocessor_Directives">Preprocessor Directives</h3>

<p>The hash mark that starts a preprocessor directive should
always be at the beginning of the line.</p>

<p>Even when preprocessor directives are within the body
of indented code, the directives should start at the
beginning of the line.</p>

<pre>// Good - directives at beginning of line
  if (lopsided_score) {
#if DISASTER_PENDING      // Correct -- Starts at beginning of line
    DropEverything();
# if NOTIFY               // OK but not required -- Spaces after #
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
</pre>

<pre class="badcode">// Bad - indented directives
  if (lopsided_score) {
    #if DISASTER_PENDING  // Wrong!  The "#if" should be at beginning of line
    DropEverything();
    #endif                // Wrong!  Do not indent "#endif"
    BackToNormal();
  }
</pre>

<h3 id="Class_Format">Class Format</h3>

<p>Sections in <code>public</code>, <code>protected</code> and
<code>private</code> order, each indented one space.</p>

<p>The basic format for a class definition (lacking the
comments, see <a href="#Class_Comments">Class
Comments</a> for a discussion of what comments are
needed) is:</p>

<pre>class MyClass : public OtherClass {
 public:      // Note the 1 space indent!
  MyClass();  // Regular 2 space indent.
  explicit MyClass(int var);
  ~MyClass() {}

  void SomeFunction();
  void SomeFunctionThatDoesNothing() {
  }

  void set_some_var(int var) { some_var_ = var; }
  int some_var() const { return some_var_; }

 private:
  bool SomeInternalFunction();

  int some_var_;
  int some_other_var_;
};
</pre>

<p>Things to note:</p>

<ul>
  <li>Any base class name should be on the same line as
  the subclass name, subject to the 80-column limit.</li>

  <li>The <code>public:</code>, <code>protected:</code>,
  and <code>private:</code> keywords should be indented
  one space.</li>

  <li>Except for the first instance, these keywords
  should be preceded by a blank line. This rule is
  optional in small classes.</li>

  <li>Do not leave a blank line after these
  keywords.</li>

  <li>The <code>public</code> section should be first,
  followed by the <code>protected</code> and finally the
  <code>private</code> section.</li>

  <li>See <a href="#Declaration_Order">Declaration
  Order</a> for rules on ordering declarations within
  each of these sections.</li>
</ul>

<h3 id="Namespace_Formatting">Namespace Formatting</h3>

<p>The contents of namespaces are not indented.</p>

<p><a href="#Namespaces">Namespaces</a> do not add an
extra level of indentation. For example, use:</p>

<pre>namespace {

void foo() {  // Correct.  No extra indentation within namespace.
  ...
}

}  // namespace
</pre>

<p>Do not indent within a namespace:</p>

<pre class="badcode">namespace {

  // Wrong!  Indented when it should not be.
  void foo() {
    ...
  }

}  // namespace
</pre>

<h3 id="Horizontal_Whitespace">Horizontal Whitespace</h3>

<p>Use of horizontal whitespace depends on location. Never put
trailing whitespace at the end of a line.</p>

<h4>General</h4>

<pre>void f(bool b) {  // Open braces should always have a space before them.
  ...
int i = 0;  // Semicolons usually have no space before them.
// Spaces inside braces for braced-init-list are optional.  If you use them,
// put them on both sides!
int x[] = { 0 };
int x[] = {0};

// Spaces around the colon in inheritance and initializer lists.
class Foo : public Bar {
 public:
  // For inline function implementations, put spaces between the braces
  // and the implementation itself.
  Foo(int b) : Bar(), baz_(b) {}  // No spaces inside empty braces.
  void Reset() { baz_ = 0; }  // Spaces separating braces from implementation.
  ...
</pre>

<p>Adding trailing whitespace can cause extra work for
others editing the same file, when they merge, as can
removing existing trailing whitespace. So: Don't
introduce trailing whitespace. Remove it if you're
already changing that line, or do it in a separate
clean-up
operation (preferably when no-one
else is working on the file).</p>

<h4>Loops and Conditionals</h4>

<pre>if (b) {          // Space after the keyword in conditions and loops.
} else {          // Spaces around else.
}
while (test) {}   // There is usually no space inside parentheses.
switch (i) {
for (int i = 0; i &lt; 5; ++i) {
// Loops and conditions may have spaces inside parentheses, but this
// is rare.  Be consistent.
switch ( i ) {
if ( test ) {
for ( int i = 0; i &lt; 5; ++i ) {
// For loops always have a space after the semicolon.  They may have a space
// before the semicolon, but this is rare.
for ( ; i &lt; 5 ; ++i) {
  ...

// Range-based for loops always have a space before and after the colon.
for (auto x : counts) {
  ...
}
switch (i) {
  case 1:         // No space before colon in a switch case.
    ...
  case 2: break;  // Use a space after a colon if there's code after it.
</pre>

<h4>Operators</h4>

<pre>// Assignment operators always have spaces around them.
x = 0;

// Other binary operators usually have spaces around them, but it's
// OK to remove spaces around factors.  Parentheses should have no
// internal padding.
v = w * x + y / z;
v = w*x + y/z;
v = w * (x + z);

// No spaces separating unary operators and their arguments.
x = -5;
++x;
if (x &amp;&amp; !y)
  ...
</pre>

<h4>Templates and Casts</h4>

<pre>// No spaces inside the angle brackets (&lt; and &gt;), before
// &lt;, or between &gt;( in a cast
std::vector&lt;std::string&gt; x;
y = static_cast&lt;char*&gt;(x);

// Spaces between type and pointer are OK, but be consistent.
std::vector&lt;char *&gt; x;
</pre>

<h3 id="Vertical_Whitespace">Vertical Whitespace</h3>

<p>Minimize use of vertical whitespace.</p>

<p>This is more a principle than a rule: don't use blank lines when
you don't have to. In particular, don't put more than one or two blank
lines between functions, resist starting functions with a blank line,
don't end functions with a blank line, and be sparing with your use of
blank lines. A blank line within a block of code serves like a
paragraph break in prose: visually separating two thoughts.</p>

<p>The basic principle is: The more code that fits on one screen, the
easier it is to follow and understand the control flow of the
program. Use whitespace purposefully to provide separation in that
flow.</p>

<p>Some rules of thumb to help when blank lines may be
useful:</p>

<ul>
  <li>Blank lines at the beginning or end of a function
  do not help readability.</li>

  <li>Blank lines inside a chain of if-else blocks may
  well help readability.</li>

  <li>A blank line before a comment line usually helps
  readability — the introduction of a new comment suggests
  the start of a new thought, and the blank line makes it clear
  that the comment goes with the following thing instead of the
  preceding.</li>

  <li>Blank lines immediately inside a declaration of a namespace or block of
  namespaces may help readability by visually separating the load-bearing
  content from the (largely non-semantic) organizational wrapper. Especially
  when the first declaration inside the namespace(s) is preceded by a comment,
  this becomes a special case of the previous rule, helping the comment to
  "attach" to the subsequent declaration.</li>
</ul>

<h2 id="Exceptions_to_the_Rules">Exceptions to the Rules</h2>

<p>The coding conventions described above are mandatory.
However, like all good rules, these sometimes have exceptions,
which we discuss here.</p>

<div>

<hr>
</div>
</body>
</html>