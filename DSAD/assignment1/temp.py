from typing import List

def search(self, company_name: str) -> List:    
    search_queue = [] # ----------------------------------------   | O(constant)
    search_queue.append(self.root)# ----------------------------   | O(constant)
    n = len(search_queue)# -------------------------------------   | O(constant)

    while n > 0:
        front = search_queue.pop(0)# ---------------------------   |
        if front.company_name == company_name:# ----------------   |
            return [True, front]# ------------------------------   |
        for subsidiary in front.acquired_companies:# -----------   |---> O(n)
            search_queue.append(subsidiary)# -------------------   |
        n = len(search_queue)# ---------------------------------   |

    return [False, "Requested company doesn't exist"]# ---------   | O(constant)

def acquire(self, parent_company: str, acquired_company: str) -> str:
    
    presence = self.search(parent_company)# ---------------------------------   | O(n)
    acquired_presence = self.search(acquired_company)# ------------------- --   | O(n)

    if not presence[0]:# ----------------------------------------------------   | O(constant)
        return f"ACQUIRED FAILED: {acquired_company} by {parent_company}"#---   | O(constant)
    elif acquired_presence[0]:# ---------------------------------------------   | O(constant)
        return f"ACQUIRED FAILED:{acquired_company} BY:{parent_company}"#----   | O(constant)
    else:# ------------------------------------------------------------------   | O(constant)
        subsidiary_company = Node(presence[1], acquired_company)#------------   | O(constant)
        presence[1].acquired_companies.append(subsidiary_company)#-----------   | O(constant)
        return f"ACQUIRED SUCCESS: {parent_company} BY:{acquired_company}"#--   | O(constant)

def detail(self, company_name: str) -> str:
    
    presence = self.search(company_name)# --------------------------------------------   | O(n)
    
    if not presence[0]:# -------------------------------------------------------------   | O(constant)
        return f"DETAIL: {company_name}\nDETAIL FAILED: {company_name} \
                    does not exist in the organizational hierarchy"# -----------------   | O(constant)
    else:# ---------------------------------------------------------------------------   | O(constant)
        company = presence[1]# -------------------------------------------------------   | O(constant)
        details_string =  f"DETAIL: {company_name}"# ---------------------------------   | O(constant)
        subsidiaries = [x.company_name for x in company.acquired_companies]# ---------   | O(constant)
        if len(subsidiaries):# -------------------------------------------------------   | O(constant)
            details_string += f"\nAcquired companies: {', '.join(subsidiaries)}"# ----   | O(constant)
            details_string += f"\nNo of companies acquired: {len(subsidiaries)}"# ----   | O(constant)
        else:# -----------------------------------------------------------------------   | O(constant)
            details_string += f"\nAcquired companies: none\nNo of \
                                companies acquired: 0"# ------------------------------   | O(constant)
    return details_string# -----------------------------------------------------------   | O(constant)

def release(self, company_name: str) -> str:
    presence = self.search(company_name)# ---------------------------------------------   | O(n)

    if not presence[0]:# --------------------------------------------------------------   | O(constant)
        return f"RELEASE FAILED: release {company_name} failed."# ---------------------   | O(constant)
    else:# -----------------------------------------------------------------------------  | O(constant)
        to_remove = presence[1]# ------------------------------------------------------   | O(constant)
        if self.root.company_name == company_name:# -----------------------------------   | O(constant)
            return f"RELEASE FAILED: cannot release the base conglomerate company"# ---   | O(constant)
        else:# ------------------------------------------------------------------------   | O(constant)
            new_subsidiaries = []            # ----------------------------------------   | O(constant)
            for subsidiary in to_remove.parent_company.acquired_companies:# -----------   | O(constant)
                if not(subsidiary.company_name == company_name):# ---------------------   | O(constant)
                    new_subsidiaries.append(subsidiary)# ------------------------------   | O(constant)
                else:
                    for grandson_subsidiary in to_remove.acquired_companies:# ---------   | O(constant)
                        grandson_subsidiary.parent_company = to_remove.parent_company#-   | O(constant)
                        new_subsidiaries.append(grandson_subsidiary)# -----------------   | O(constant)

            to_remove.parent_company.acquired_companies = new_subsidiaries# -----------   | O(constant)
        return f"RELEASE SUCCESS: released {company_name} successfully."# -------------   | O(constant)

