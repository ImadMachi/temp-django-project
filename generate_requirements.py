import os
import ast
import pkg_resources


def get_imports(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        # Remove null bytes
        content = content.replace("\0", "")

        tree = ast.parse(content)

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:  # absolute import
                    imports.add(node.module.split(".")[0])
        return imports
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return set()


def get_project_imports(directory):
    imports = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_imports = get_imports(os.path.join(root, file))
                imports.update(file_imports)
    return imports


def get_installed_packages():
    return {pkg.key: pkg for pkg in pkg_resources.working_set}


def main():
    project_dir = "."  # Current directory
    project_imports = get_project_imports(project_dir)
    installed_packages = get_installed_packages()

    requirements = []
    for imp in project_imports:
        if imp in installed_packages:
            pkg = installed_packages[imp]
            requirements.append(f"{pkg.key}=={pkg.version}")
        else:
            print(f"Warning: '{imp}' not found in installed packages.")

    with open("requirements.txt", "w") as f:
        for req in sorted(requirements):
            f.write(req + "\n")

    print("requirements.txt has been generated.")


if __name__ == "__main__":
    main()
