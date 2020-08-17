# project_mgt
This project is a project management system. According to the Project Management Institute a project is a *"temporary endeavor undertaken to create a unique product, service or result"* [PMI](https://www.pmi.org/about/learn-about-pmi/what-is-project-management#:~:text=A%20project%20is%20temporary%20in,therefore%20defined%20scope%20and%20resources.&text=Project%20management%2C%20then%2C%20is%20the,to%20meet%20the%20project%20requirements.) 

## Apps
### project_mgt
The **project_mgt** app is the core app containing the settings.py  and top-level urls.py files.

### projects
The **projects** app contains the **project and deliverable** models.

### persons
The **persons** app contains the **person** model.

### pages
The **pages** app contains the pages that don't leverage of a model such as the about and home page.

### customers
The **customers** app contains the **customer** model.

## Models
The following models are used in this project.

### Project
The **Project** model connects the components of the project to Customer to produce the project Scope (work required to create the project Deliverables). A project has a defined start and end dates. 

### Deliverable
The **Deliverable** model is a product or service that a project produces for its customer.

### Milestone
The **Milestone** model *to be implemented.*

### Action
The **Action** model *to be implemented.*

### Person
The **Person** model is a base class.

### Stakeholder
The **Stakeholder** model *to be implemented. Will be a subclass of the person model.*

### Customer
The **Customer** model is the recipient of the project.

### Address
The **Address** model *to be implemented. Will be contain address and contact details.*
