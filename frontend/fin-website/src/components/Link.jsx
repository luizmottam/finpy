import { Link } from "react-router-dom";

function CustomLink({ to, children, className }) {
  return (
    <Link to={to} className={className}>
      <span className={className}>{children}</span>
    </Link>
  );
}

export default CustomLink;
