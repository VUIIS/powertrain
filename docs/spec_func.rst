The Problem & Goals of Powertrain
=================================

Powertrain is written for researchers using MR imaging at Vanderbilt. While ideas implemented within Powertrain may have broad applicability, we are designing Powertrain to be most useful to Vanderbilt researchers who capture MR data at `VUIIS <http://vuiis.vanderbilt.edu>`_. This is not a generalized system for running large-scale imaging analyses; we will make design & implementation decisions specific to infrastructure available at Vanderbilt. If similar infrastructure is available elsewhere, other research engineers may find Powertrain useful.

The Problem
+++++++++++

Data management (DM) of large neuroimaging projects is wide-ranging & difficult. Some things to consider:

* Storage & archival of raw data.
* Storage & processing of analyzed data.
* Linkability between MR data and subject demographics and/or out-of- or in-magnet behavioral tasks.
* Data provenance

Unfortunately poor DM planning & implementation can ruin projects and good DM is difficult to design and more difficult to achieve. However, good DM enables quite a few features important to a projects success including:

* Automatically-generated subject- and group-level analyses
* Integrated data security & backup
* Sharing of best practices with respect to neuroimaging analyses
* Reduced costs of equipment & personnel

The majority of laboratories running neuroimaging experiments consider & run each project separately. Different people, computer resources & standard operating procedures all decrease replicability & reproducibility and increase costs. More advanced labs may develop software and resources to manage their studies together. Rarely do they consider how other labs might operate.

The principle idea behind Powertrain is that at a high level, all neuroimaging studies are the same and can be modeled appropriately. Given such a model, proper data management should be a service executed at the institution level. Only at this level can resources be optimally used & shared among all users.