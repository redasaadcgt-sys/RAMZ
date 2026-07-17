import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LanguageReference() {

    const navigate = useNavigate();

    const [search, setSearch] = useState("");

    const items = [
        "Overview",
        "Comments",
        "Output",
        "Datatypes",
        "Variables",
        "Constants",
        "Operations",
        "Conditional Statements",
        "Loops",
        "Functions"
    ];


    const filteredItems = items.filter(item =>
        item.toLowerCase().includes(search.toLowerCase())
    );


    const handleNavigation = (item) => {

        if (item === "Overview") {
            navigate("/");

            setTimeout(() => {
                const main = document.querySelector("main");

                if (main) {
                    main.scrollTop = 0;
                }
            }, 100);

            return;
        }

        const section = item
            .toLowerCase()
            .replaceAll(" ", "-");

        navigate(`/syntax#${section}`);

        setTimeout(() => {
            const element = document.getElementById(section);

            if (element) {
                element.scrollIntoView({
                    block: "start"
                });
            }
        }, 100);
    };

    return (
        <div className="h-100 d-flex flex-column">

            <h5 className="responsive-reference-title fw-bold text-dark mb-3">
                RAMZ Reference
            </h5>


            <input
                type="text"
                className="form-control form-control-sm mb-3"
                placeholder="Search..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />


            <div className="overflow-auto flex-grow-1">

                <ul className="list-unstyled">

                    {filteredItems.map((item) => (

                        <li key={item}>

                            <button
                                onClick={() => handleNavigation(item)}
                                className="
                                    w-100
                                    text-start
                                    border-0
                                    bg-transparent
                                    py-2
                                    px-2
                                    rounded
                                    responsive-sidebar-text
                                    text-secondary
                                    "
                            >
                                {item}
                            </button>

                        </li>

                    ))}

                </ul>

            </div>

        </div>
    );
}

export default LanguageReference;