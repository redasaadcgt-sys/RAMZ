import LanguageReference from '../components/LanguageReference';

function MainPage() {
    
    return (


            <div className="h-100 d-flex flex-column">

                {/* Main Content */}
                <main className="h-100 d-flex flex-column">

                    {/* Hero Section */}
                    <section>

                        <div className="d-flex align-items-center gap-3 mb-3">

                            <h1 className="responsive-title fw-bold text-dark mb-0">
                                Welcome to <span className="text-primary">RAMZ</span>
                            </h1>

                            <div className="rounded overflow-hidden shadow-sm">

                                <img
                                src={`${import.meta.env.BASE_URL}Images/logo.png`}
                                    alt="RAMZ logo"
                                    className="img-fluid"
                                    style={{
                                        maxHeight: "clamp(40px, 8vw, 80px)",
                                        maxWidth: "clamp(40px, 8vw, 80px)",
                                        objectFit: "contain"
                                    }}
                                />

                            </div>

                        </div>


                        <p className="responsive-lead text-secondary">

                            RAMZ is an open-source programming language created by
                            <strong> Reda Saad</strong>, built using{" "}
                            <span className="text-success">
                                Python
                            </span>
                            {" "}and{" "}
                            <span className="text-success">
                                C
                            </span>.
                            It provides a modern, customizable, and scalable
                            programming experience for developers.

                        </p>


                        {/* Image Panel */}
                        <div className="my-4">

                            <div className="rounded overflow-hidden shadow-sm">

                            <div className="responsive-image-container">
                                <img
                                    src={`${import.meta.env.BASE_URL}Images/overview.png`}
                                    alt="RAMZ programming language"
                                    className="img-fluid"
                                />
                            </div>

                            </div>


                            <p className="responsive-small text-muted mt-2">
                                Basic RAMZ program example.
                            </p>

                        </div>

                    </section>


                    <hr className="my-4" />


                    {/* About */}
                    <section>

                        <h3 className="responsive-heading fw-semibold text-dark mt-4">
                            About RAMZ
                        </h3>


                        <p className="responsive-text text-secondary">
                            RAMZ follows standard programming language syntax
                            principles while providing powerful features for
                            developers. It includes a built-in debugging system
                            designed to make development and troubleshooting
                            easier.
                        </p>


                        <p className="responsive-text text-secondary">
                            The language is fully customizable and scalable,
                            allowing developers to adapt it for different types
                            of projects and environments.
                        </p>

                    </section>


                    {/* Getting Started */}
                    <section>

                        <h3 className="responsive-heading fw-semibold text-dark mt-5">
                            Getting Started
                        </h3>


                        <p className="responsive-text text-secondary">
                            To set up RAMZ, download the compiler from the
                            official repository and make sure your system has
                            the required development tools installed.
                        </p>


                        <ul className="responsive-text text-secondary ps-3">

                            <li className="mb-2">
                                Python environment/toolchain
                            </li>

                            <li className="mb-2">
                                LLVM toolchain
                            </li>

                            <li className="mb-2">
                                RAMZ compiler package
                            </li>

                        </ul>


                        <div className="bg-white border rounded p-4 my-4">

                            <h5 className="responsive-text text-primary fw-semibold">
                                Installation Process
                            </h5>


                            <p className="responsive-text text-secondary mb-0">

                                After downloading the compiler, run the included
                                setup script and the environment will be ready
                                for development.

                            </p>

                        </div>

                    </section>


                    {/* Features */}
                    <section>

                        <h3 className="responsive-heading fw-semibold text-dark mt-5">
                            Features
                        </h3>


                        <ul className="responsive-text text-secondary ps-3">

                            <li className="mb-2">
                                Clean and standard syntax
                            </li>

                            <li className="mb-2">
                                Built-in debugging support
                            </li>

                            <li className="mb-2">
                                Fully customizable architecture
                            </li>

                            <li className="mb-2">
                                Scalable for different projects
                            </li>

                            <li className="mb-2">
                                Open-source development
                            </li>

                        </ul>

                    </section>


                    {/* Developer */}
                    <section className="mt-5 pb-5">

                        <h3 className="responsive-heading fw-semibold text-dark">
                            Developer
                        </h3>


                        <p className="responsive-text text-secondary">
                            RAMZ is created and maintained by Reda Saad.
                        </p>


                        <a
                            href="https://www.linkedin.com/in/reda-saad-659307415"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-primary fw-semibold text-decoration-none responsive-text"
                        >
                            Visit Reda Saad's LinkedIn →
                        </a>

                    </section>

                </main>

            </div>

    );
}

export default MainPage;

