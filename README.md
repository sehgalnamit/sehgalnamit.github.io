# namitsehgal-site

Welcome to the **namitsehgal-site** project! This repository hosts a website for publishing articles and guides. Below are the details and instructions for setting up and linking your custom domain.

## Project Structure

The project consists of the following files and directories:

- **_config.yml**: Configuration settings for the site, including title and metadata.
- **CNAME**: Specifies the custom domain name (namitsehgal.com) for the GitHub Pages site.
- **index.md**: Main content file for the homepage, written in Markdown.
- **_posts/**: Contains blog posts in Markdown format.
- **_layouts/**: Defines the HTML layout for the site.
- **_includes/**: Contains reusable HTML code for the head section.
- **assets/**: Contains CSS and JavaScript files for styling and interactivity.
- **.github/**: Contains GitHub Actions workflow configuration for deployment.
- **.gitignore**: Specifies files to be ignored by Git.
- **README.md**: Documentation for the project.

## Steps to Create the GitHub Repository and Link Your Domain

1. **Create a GitHub Repository:**
   - Go to GitHub and create a new repository named `namitsehgal-site`.
   - Initialize it with a README file.

2. **Clone the Repository:**
   - Clone the repository to your local machine using the command:
     ```
     git clone https://github.com/yourusername/namitsehgal-site.git
     ```

3. **Add Project Files:**
   - Create the project structure as outlined above in the cloned repository.
   - Add the necessary files and content.

4. **Push Changes to GitHub:**
   - Add, commit, and push your changes:
     ```
     git add .
     git commit -m "Initial commit"
     git push origin main
     ```

5. **Configure GitHub Pages:**
   - Go to the repository settings on GitHub.
   - Scroll down to the "GitHub Pages" section.
   - Select the branch (usually `main`) and the root folder for the source.

6. **Link Your Domain:**
   - In the `CNAME` file, add your custom domain name: `namitsehgal.com`.
   - Go to your domain registrar (e.g., porkbun.com) and set up a CNAME record pointing to `yourusername.github.io`.

7. **Wait for DNS Propagation:**
   - It may take some time for the DNS changes to propagate. After that, your site should be accessible at `namitsehgal.com`.

8. **Verify the Setup:**
   - Visit your domain to ensure that it correctly points to your GitHub Pages site.

By following these steps, you will have your website hosted on GitHub and linked to your custom domain. Happy publishing!# Workflow trigger - 2026-05-25 13:19:10
