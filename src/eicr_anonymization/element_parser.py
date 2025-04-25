from lxml.etree import _Element


def has_text(element: _Element) -> bool:
    """Check if the XML element has text content.

    Args:
        element: The XML element to check.

    Returns:
        bool: True if the element has text content, False otherwise.
    """
    return element.text is not None and element.text.strip() != ""


class Element:
    """Class representing an XML element with its attributes and text content."""

    def __init__(self, element: _Element, cda_type: str):
        """Initialize the Element with its attributes and text content."""
        self.name = element.tag

        self.attributes = {}
        for attribute in element.items():
            self.attributes[attribute[0]] = attribute[1]
        self.cda_type = cda_type
        self.text = element.text
        self.path = element.getroottree().getpath(element)

    def __repr__(self) -> str:
        """Get a string representation of the tag."""
        root_tag = str(self.name).removeprefix("{urn:hl7-org:v3}")
        repr = f"{self.cda_type}: <{root_tag}"
        for key, value in self.attributes.items():
            root_key = key.removeprefix("{http://www.w3.org/2001/XMLSchema-instance}")
            repr += f' {root_key}="{value}"'

        if self.text:
            repr += f">{self.text.strip()}</{root_tag}>"
        else:
            repr += " />"

        return repr


class Parser:
    """Class for finding sensitive elements in an XML document."""

    def __init__(self):
        """Initialize the Parser with an empty list of sensitive elements."""
        self.sensitive_elements: list[Element] = []

    def find_sensitive_elements(self, element: _Element):
        """Find sensitive elements in the XML document.

        Args:
            element: The XML element to parse.
        """
        if element.tag == "{urn:hl7-org:v3}ClinicalDocument":
            self.parse_ClinicalDocument(element)
        else:
            raise ValueError(f"Unknown root element: {element.tag}")

        return self.sensitive_elements

    def add_sensitive_element(self, element: _Element, cda_type: str):
        """Add a sensitive element to the list."""
        self.sensitive_elements.append(Element(element, cda_type))

    def parse_ClinicalDocument(self, element: _Element):
        """Logical Model: ClinicalDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ClinicalDocument.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code" | "{urn:hl7-org:v3}confidentialityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}recordTarget":
                    self.parse_RecordTarget(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}dataEnterer":
                    self.parse_DataEnterer(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}custodian":
                    self.parse_Custodian(child)
                case "{urn:hl7-org:v3}informationRecipient":
                    self.parse_InformationRecipient(child)
                case "{urn:hl7-org:v3}authenticator":
                    self.parse_Authenticator(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant1(child)
                case "{urn:hl7-org:v3}inFulfillmentOf":
                    self.parse_InFulfillmentOf(child)
                case "{urn:hl7-org:v3}documentationOf":
                    self.parse_DocumentationOf(child)
                case "{urn:hl7-org:v3}relatedDocument":
                    self.parse_RelatedDocument(child)
                case "{urn:hl7-org:v3}authorization":
                    self.parse_Authorization(child)
                case "{urn:hl7-org:v3}componentOf":
                    self.parse_ComponentOf(child)
                case "{urn:hl7-org:v3}component":
                    self.parse_Component(child)

    def parse_CE(self, element: _Element):
        """Logical Model: CE: CodedWithEquivalents (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CE.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}orginalText":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}translation":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}effectiveTime" | "{urn:hl7-org:v3}copyTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}RecordTarget":
                    self.parse_RecordTarget(child)

    def parse_ED(self, element: _Element):
        """Logical Model: ED: EncapsulatedData (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ED.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "ED")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}reference":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}thumbnail":
                    self.parse_ED(child)

    def parse_TEL(self, element: _Element):
        """Parse a TEL (Telecommunication) XML element."""
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "TEL")

        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}useablePeriod":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "IVXB_TS":
                            self.parse_EIVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "SXPR_TS" | None:
                            self.parse_SXPR_TS(child)
                        case _:
                            raise ValueError(
                                f"Unknown type: {child.get('{http://www.w3.org/2001/XMLSchema-instance}type')}"
                            )

    def parse_IVL_TS(self, element: _Element):
        """Logical Model: IVL_TS: Interval (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "IVL_TS")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}low" | "{urn:hl7-org:v3}high":
                    self.parse_IVXB_TS(child)
                case "{urn:hl7-org:v3}center":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}width":
                    self.parse_PQ(child)

    def parse_IVXB_TS(self, element: _Element):
        """Logical Model: IVXB_TS: Interval Boundary PointInTime (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "IVXB_TS")

    def parse_TS(self, element: _Element):
        """Logical Model: TS: PointInTime (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "TS")

    def parse_PQ(self, element: _Element):
        """Parse a PQ (Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}translation":
                    self.parse_PQR(child)

    def parse_PQR(self, element: _Element):
        """Handle a PQR (Quantity Range) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}orginalText":
                    self.parse_ED(child)

    def parse_EIVL_TS(self, element: _Element):
        """Parse an EIVL_TS (Explicit Interval Timestamp) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}event":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}offset":
                    self.parse_IVL_PQ(child)

    def parse_IVL_PQ(self, element: _Element):
        """Parse an IVL_PQ (Interval Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}low" | "{urn:hl7-org:v3}high":
                    self.parse_IVXB_PQ(child)
                case "{urn:hl7-org:v3}center" | "{urn:hl7-org:v3}width":
                    self.parse_PQ(child)

    def parse_IVXB_PQ(self, element: _Element):
        """Parse an IVXB_PQ (Interval Bound Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}translation":
                    self.parse_PQR(child)

    def parse_PIVL_TS(self, element: _Element):
        """Parse a PIVL_TS (Periodic Interval Timestamp) XML element."""
        # PIVL_TS should not have a value attribute, however the 3.1 example eICR has it
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "PIVL_TS!")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}phase":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}period":
                    self.parse_PQ(child)

    def parse_SXPR_TS(self, element: _Element):
        """Logical Model: SXPR_TS: Component part of GTS (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXPR-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "SXPR_TS")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}COMP":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "IVXB_TS":
                            self.parse_EIVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "SXPR_TS" | None:
                            self.parse_SXPR_TS(child)
                        case _:
                            raise ValueError(
                                f"Unknown type: {child.get('{http://www.w3.org/2001/XMLSchema-instance}type')}"
                            )

    def parse_CD(self, element: _Element):
        """Logical Model: CD: ConceptDescriptor (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CD.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}originalText":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}qualifier":
                    self.parse_CR(child)
                case "{urn:hl7-org:v3}translation":
                    self.parse_CD(child)

    def parse_CR(self, element: _Element):
        """Logical Model: CR: ConceptRole (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CR.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_CV(child)
                case "{urn:hl7-org:v3}value":
                    self.parse_CD(child)

    def parse_CV(self, element: _Element):
        """Logical Model: CV: CodedValue (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CV.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}originalText":
                    self.parse_ED(child)

    def parse_RecordTarget(self, element: _Element):
        """Logical Model: RecordTarget (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RecordTarget.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}patientRole":
                    self.parse_PatientRole(child)

    def parse_PatientRole(self, element: _Element):
        """Logical Model: PatientRole (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PatientRole.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identfiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}patient":
                    self.parse_Patient(child)
                case "{urn:hl7-org:v3}providerOrganization":
                    self.parse_Organization(child)

    def parse_II(self, element: _Element):
        """Logical Model: II: InstanceIdentifier (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-II.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "extension":
                    self.add_sensitive_element(element, "II")

    def parse_IdentifiedBy(self, element: _Element):
        """Logical Model: IdentifiedBy (CDA Class) ( Abstract ).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IdentifiedBy.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}alterateIdentification":
                    self.parse_AlternateIdentification(child)

    def parse_AlternateIdentification(self, element: _Element):
        """Logical Model: AlternateIdentification (CDA Class) ( Abstract ).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AlternateIdentification.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)

    def parse_AD(self, element: _Element):
        """Logical Model: AD: PostalAddress (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AD.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "AD")
        for child in element:
            match child.tag:
                case (
                    "{urn:hl7-org:v3}country"
                    | "{urn:hl7-org:v3}state"
                    | "{urn:hl7-org:v3}county"
                    | "{urn:hl7-org:v3}city"
                    | "{urn:hl7-org:v3}postalCode"
                    | "{urn:hl7-org:v3}streetAddressLine"
                    | "{urn:hl7-org:v3}houseNumber"
                    | "{urn:hl7-org:v3}direction"
                    | "{urn:hl7-org:v3}streetName"
                    | "{urn:hl7-org:v3}streetNameBase"
                    | "{urn:hl7-org:v3}streetNameType"
                    | "{urn:hl7-org:v3}additionalLocator"
                    | "{urn:hl7-org:v3}unitID"
                    | "{urn:hl7-org:v3}unitType"
                    | "{urn:hl7-org:v3}careOf"
                    | "{urn:hl7-org:v3}censusTract"
                    | "{urn:hl7-org:v3}deliveryAddressLine"
                    | "{urn:hl7-org:v3}deliveryInstallationType"
                    | "{urn:hl7-org:v3}deliveryInstallationArea"
                    | "{urn:hl7-org:v3}deliveryInstallationQualifier"
                    | "{urn:hl7-org:v3}deliveryMode"
                    | "{urn:hl7-org:v3}deliveryModeIdentifier"
                    | "{urn:hl7-org:v3}buildingNumberSuffix"
                    | "{urn:hl7-org:v3}postBox"
                    | "{urn:hl7-org:v3}precinct"
                ):
                    self.parse_ADXP(child)
                case "{urn:hl7-org:v3}useablePeriod":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "IVXB_TS":
                            self.parse_EIVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "SXPR_TS" | None:
                            self.parse_SXPR_TS(child)
                        case _:
                            raise ValueError(
                                f"Unknown type: {child.get('{http://www.w3.org/2001/XMLSchema-instance}type')}"
                            )

    def parse_ADXP(self, element: _Element):
        """Logical Model: ADXP: CharacterString (V3 Data Type) .

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ADXP.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "ADXP")

    def parse_Patient(self, element: _Element):
        """Logical Model: Patient (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Patient.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                case (
                    "{urn:hl7-org:v3}administrativeGenderCode"
                    | "{urn:hl7-org:v3}materialStatusCode"
                    | "{urn:hl7-org:v3}religiousAffiliationCode"
                    | "{urn:hl7-org:v3}raceCode"
                    | "{urn:hl7-org:v3}ethnicGroupCode"
                    | "{urn:hl7-org:v3}languageCommunication"
                ):
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}birthTime" | "{urn:hl7-org:v3}deceasedTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}guardian":
                    self.parse_Guardian(child)
                case "{urn:hl7-org:v3}birthplace":
                    self.parse_Birthplace(child)

    def parse_PN(self, element: _Element):
        """Logical Model: PN: PersonName (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PN.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "PN")
        for child in element:
            match child.tag:
                case (
                    "{urn:hl7-org:v3}family"
                    | "{urn:hl7-org:v3}given"
                    | "{urn:hl7-org:v3}prefix"
                    | "{urn:hl7-org:v3}suffix"
                ):
                    self.parse_ENXP(child)
                case "{urn:hl7-org:v3}validTime":
                    self.parse_IVL_TS(child)

    def parse_ENXP(self, element: _Element):
        """Logical Model: ENXP: Entity Name Part (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ENXP.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "ENXP")

    def parse_Guardian(self, element: _Element):
        """Logical Model: Guardian (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Guardian.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}guardianPerson":
                    self.parse_Person(child)
                case "{urn:hl7-org:v3}guardianOrganization":
                    self.parse_Organization(child)

    def parse_Person(self, element: _Element):
        """Logical Model: Person (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Person.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                case "{urn:hl7-org:v3}asPatientRelationship":
                    self.parse_CE(child)

    def parse_Birthplace(self, element: _Element):
        """Logical Model: Birthplace (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Birthplace.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}place":
                    self.parse_Place(child)

    def parse_Place(self, element: _Element):
        """Logical Model: Place (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Place.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_EN(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)

    def parse_EN(self, element: _Element):
        """Logical Model: EN: EntityName (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EN.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "EN")
        for child in element:
            match child.tag:
                case (
                    "{urn:hl7-org:v3}family"
                    | "{urn:hl7-org:v3}given"
                    | "{urn:hl7-org:v3}prefix"
                    | "{urn:hl7-org:v3}suffix"
                ):
                    self.parse_ENXP(child)
                case "{urn:hl7-org:v3}validTime":
                    self.parse_IVL_TS(child)

    def parse_Organization(self, element: _Element):
        """Logical Model: Organization (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Organization.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}name":
                    self.parse_ON(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}standardIndustryClassCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}asOrganizationPartOf":
                    self.parse_OrganizationPartOf(child)

    def parse_ON(self, element: _Element):
        """Logical Model: ON: OrganizationName (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ON.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "EN")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}prefix" | "{urn:hl7-org:v3}suffix":
                    self.parse_ENXP(child)
                case "{urn:hl7-org:v3}validTime":
                    self.parse_IVL_TS(child)

    def parse_OrganizationPartOf(self, element: _Element):
        """Logical Model: OrganizationPartOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-OrganizationPartOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}wholeOrganization":
                    self.parse_Organization(child)

    def parse_Author(self, element: _Element):
        """Logical Model: Author (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Author.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}functionCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}time":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}assignedAuthor":
                    self.parse_AssignedAuthor(child)

    def parse_AssignedAuthor(self, element: _Element):
        """Logical Model: AssignedAuthor (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedAuthor.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}assignedPerson":
                    self.parse_Person(child)
                case "{urn:hl7-org:v3}assignedAuthoringDevice":
                    self.parse_AuthoringDevice(child)
                case "{urn:hl7-org:v3}representedOrganization":
                    self.parse_Organization(child)

    def parse_AuthoringDevice(self, element: _Element):
        """Logical Model: AuthoringDevice (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AuthoringDevice.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}asMaintainedEntity":
                    self.parse_MaintainedEntity(child)

    def parse_MaintainedEntity(self, element: _Element):
        """Logical Model: MaintainedEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-MaintainedEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}maintaingPerson":
                    self.parse_Person(child)

    def parse_DataEnterer(self, element: _Element):
        """Logical Model: DataEnterer (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-DataEnterer.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}time":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}assignedEntity":
                    self.parse_AssignedEntity(child)

    def parse_AssignedEntity(self, element: _Element):
        """Logical Model: AssignedEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}assignedPerson":
                    self.parse_Person(child)
                case "{urn:hl7-org:v3}representedOrganization":
                    self.parse_Organization(child)

    def parse_Informant(self, element: _Element):
        """Logical Model: Informant (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Informant.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}assignedEntity":
                    self.parse_AssignedEntity(child)
                case "{urn:hl7-org:v3}relatedEntity":
                    self.parse_RelatedEntity(child)

    def parse_RelatedEntity(self, element: _Element):
        """Logical Model: RelatedEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}relatedPerson":
                    self.parse_Person(child)

    def parse_Custodian(self, element: _Element):
        """Logical Model: Custodian (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Custodian.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}assignedCustodian":
                    self.parse_AssignedCustodian(child)

    def parse_AssignedCustodian(self, element: _Element):
        """Logical Model: AssignedCustodian (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedCustodian.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}representedCustodianOrganization":
                    self.parse_CustodianOrganization(child)

    def parse_CustodianOrganization(self, element: _Element):
        """Logical Model: CustodianOrganization (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CustodianOrganization.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}name":
                    self.parse_ON(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)

    def parse_InformationRecipient(self, element: _Element):
        """Logical Model: InformationRecipient (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InformationRecipient.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}intendedRecipient":
                    self.parse_IntendedRecipient(child)

    def parse_IntendedRecipient(self, element: _Element):
        """Logical Model: IntendedRecipient (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IntendedRecipient.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}IdentifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}informationRecipient":
                    self.parse_Person(child)
                case "{urn:hl7-org:v3}receivedOrganization":
                    self.parse_Organization(child)

    def parse_Authenticator(self, element: _Element):
        """Logical Model: Authenticator (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Authenticator.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}time":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}signatureText":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}assignedEntity":
                    self.parse_AssignedEntity(child)

    def parse_Participant1(self, element: _Element):
        """Logical Model: Participant1 (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Participant1.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}functionCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}time":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}associatedEntity":
                    self.parse_AssociatedEntity(child)

    def parse_AssociatedEntity(self, element: _Element):
        """Logical Model: AssociatedEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssociatedEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}associatedPerson":
                    self.parse_Person(child)
                case "{urn:hl7-org:v3}scopingOrganization":
                    self.parse_Organization(child)

    def parse_InFulfillmentOf(self, element: _Element):
        """Logical Model: InFulfillmentOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InFulfillmentOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}order":
                    self.parse_Order(child)

    def parse_Order(self, element: _Element):
        """Logical Model: Order (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Order.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code" | "{urn:hl7-org:v3}priorityCode":
                    self.parse_CE(child)

    def parse_DocumentationOf(self, element: _Element):
        """Logical Model: DocumentationOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-DocumentationOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}serviceEvent":
                    self.parse_ServiceEvent(child)

    def parse_ServiceEvent(self, element: _Element):
        """Logical Model: ServiceEvent (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ServiceEvent.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer1(child)

    def parse_Performer1(self, element: _Element):
        """Logical Model: Performer1 (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Performer1.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}functionCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}time":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}assignedEntity":
                    self.parse_AssignedEntity(child)

    def parse_RelatedDocument(self, element: _Element):
        """Logical Model: RelatedDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedDocument.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}parentDocument":
                    self.parse_ParentDocument(child)

    def parse_ParentDocument(self, element: _Element):
        """Logical Model: ParentDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ParentDocument.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)

    def parse_Authorization(self, element: _Element):
        """Logical Model: Authorization (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Authorization.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}consent":
                    self.parse_Consent(child)

    def parse_Consent(self, element: _Element):
        """Logical Model: Consent (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Consent.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)

    def parse_ComponentOf(self, element: _Element):
        """Logical Model: ComponentOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ComponentOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}encompassingEncounter":
                    self.parse_EncompassingEncounter(child)

    def parse_EncompassingEncounter(self, element: _Element):
        """Logical Model: EncompassingEncounter (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EncompassingEncounter.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case (
                    "{urn:hl7-org:v3}admissionReferralSourceCode"
                    | "{urn:hl7-org:v3}dischargeDispositionCode"
                ):
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}responsibleParty":
                    for rp_child in child:
                        match rp_child.tag:
                            case "{urn:hl7-org:v3}assignedEntity":
                                self.parse_AssignedEntity(rp_child)
                case "{urn:hl7-org:v3}encounterParticipant":
                    self.parse_EncounterParticipant(child)
                case "{urn:hl7-org:v3}location":
                    for ep_child in child:
                        match ep_child.tag:
                            case "{urn:hl7-org:v3}healthCareFacility":
                                self.parse_HealthCareFacility(ep_child)

    def parse_EncounterParticipant(self, element: _Element):
        """Logical Model: EncounterParticipant (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EncounterParticipant.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}time":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}associatedEntity":
                    self.parse_AssociatedEntity(child)

    def parse_HealthCareFacility(self, element: _Element):
        """Logical Model: HealthCareFacility (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-HealthCareFacility.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}location":
                    self.parse_Place(child)
                case "{urn:hl7-org:v3}serviceProviderOrganization":
                    self.parse_Organization(child)

    def parse_Component(self, element: _Element):
        """Logical Model: Component (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Component.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}nonXMLBody":
                    self.parse_NonXMLBody(child)
                case "{urn:hl7-org:v3}structuredBody":
                    self.parse_StructuredBody(child)

    def parse_NonXMLBody(self, element: _Element):
        """Logical Model: NonXMLBody (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-NonXMLBody.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}confidentialityCode":
                    self.parse_CE(child)

    def parse_StructuredBody(self, element: _Element):
        """Logical Model: StructuredBody (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-StructuredBody.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}confidentialityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}component":
                    for c_child in child:
                        match c_child.tag:
                            case "{urn:hl7-org:v3}section":
                                self.parse_Section(c_child)

    def parse_Section(self, element: _Element):
        """Logical Model: Section (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Section.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_xhtml(child)
                case "{urn:hl7-org:v3}confidentialityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}entry":
                    self.parse_Entry(child)
                case "{urn:hl7-org:v3}component":
                    for c_child in child:
                        match c_child.tag:
                            case "{urn:hl7-org:v3}section":
                                self.parse_Section(c_child)

    def parse_xhtml(self, element: _Element):
        """XHTML Content.

        https://hl7.org/fhir/R5/narrative.html#xhtml
        """
        self.add_sensitive_element(element, "xhtml")

    def parse_Subject(self, element: _Element):
        """Logical Model: Subject (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Subject.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}awarenessCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}relatedSubject":
                    self.parse_RelatedSubject(child)

    def parse_RelatedSubject(self, element: _Element):
        """Logical Model: RelatedSubject (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedSubject.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_SubjectPerson(child)

    def parse_SubjectPerson(self, element: _Element):
        """Logical Model: SubjectPerson (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SubjectPerson.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}administrativeGenderCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}birthTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}deceasedTime":
                    self.parse_TS(child)

    def parse_Entry(self, element: _Element):
        """Logical Model: Entry (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Entry.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}act":
                    self.parse_Act(child)
                case "{urn:hl7-org:v3}encounter":
                    self.parse_Encounter(child)
                case "{urn:hl7-org:v3}observation":
                    self.parse_Observation(child)
                case "{urn:hl7-org:v3}organizer":
                    self.parse_Organizer(child)
                case "{urn:hl7-org:v3}procedure":
                    self.parse_Procedure(child)
                case "{urn:hl7-org:v3}regionOfInterest":
                    self.parse_RegionOfInterest(child)
                case "{urn:hl7-org:v3}substanceAdministration":
                    self.parse_SubstanceAdministration(child)
                case "{urn:hl7-org:v3}supply":
                    self.parse_Supply(child)

    def parse_Act(self, element: _Element):
        """Logical Model: Act (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Act.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}priorityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_Specimen(self, element: _Element):
        """Logical Model: Specimen (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Specimen.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}specimenRole":
                    self.parse_SpecimenRole(child)

    def parse_SpecimenRole(self, element: _Element):
        """Logical Model: SpecimenRole (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SpecimenRole.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}specimenPlayingEntity":
                    self.parse_SpecimenPlayingEntity(child)

    def parse_SpecimenPlayingEntity(self, element: _Element):
        """Logical Model: SpecimenPlayingEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SpecimenPlayingEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}quantity":
                    self.parse_PQ(child)
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                case "{urn:hl7-org:v3}birthTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)

    def parse_Performer2(self, element: _Element):
        """Logical Model: Performer2 (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Performer2.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}functionCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}time":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}assignedEntity":
                    self.parse_AssignedEntity(child)

    def parse_Participant2(self, element: _Element):
        """Logical Model: Participant2 (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Participant2.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}functionCode" | "{urn:hl7-org:v3}awarenessCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}time":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}participantRole":
                    self.parse_ParticipantRole(child)

    def parse_ParticipantRole(self, element: _Element):
        """Logical Model: ParticipantRole (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ParticipantRole.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}playingDevice":
                    self.parse_Device(child)
                case "{urn:hl7-org:v3}playingEntity":
                    self.parse_PlayingEntity(child)
                case "{urn:hl7-org:v3}scopingEntity":
                    self.parse_Entity(child)

    def parse_Device(self, element: _Element):
        """Logical Model: Device (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Device.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)

    def parse_PlayingEntity(self, element: _Element):
        """Logical Model: PlayingEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PlayingEntity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}quantity":
                    self.parse_PQ(child)
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                case "{urn:hl7-org:v3}birthTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)

    def parse_Entity(self, element: _Element):
        """Logical Model: Entity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Entity.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)

    def parse_EntryRelationship(self, element: _Element):
        """Logical Model: EntryRelationship (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EntryRelationship.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}act":
                    self.parse_Act(child)
                case "{urn:hl7-org:v3}encounter":
                    self.parse_Encounter(child)
                case "{urn:hl7-org:v3}observation":
                    self.parse_Observation(child)
                case "{urn:hl7-org:v3}observationMedia":
                    self.parse_ObservationMedia(child)
                case "{urn:hl7-org:v3}organizer":
                    self.parse_Organizer(child)
                case "{urn:hl7-org:v3}procedure":
                    self.parse_Procedure(child)
                case "{urn:hl7-org:v3}regionOfInterest":
                    self.parse_RegionOfInterest(child)
                case "{urn:hl7-org:v3}substanceAdministration":
                    self.parse_SubstanceAdministration(child)
                case "{urn:hl7-org:v3}supply":
                    self.parse_Supply(child)

    def parse_Encounter(self, element: _Element):
        """Logical Model: Encounter (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Encounter.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}dischargeDispositionCode" | "{urn:hl7-org:v3}priorityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_Reference(self, element: _Element):
        """Logical Model: Reference (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Reference.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}externalAct":
                    self.parse_ExternalAct(child)
                case "{urn:hl7-org:v3}externalObservation":
                    self.parse_ExternalObservation(child)
                case "{urn:hl7-org:v3}externalProcedure":
                    self.parse_ExternalProcedure(child)
                case "{urn:hl7-org:v3}externalDocument":
                    self.parse_ExternalDocument(child)

    def parse_ExternalAct(self, element: _Element):
        """Logical Model: ExternalAct (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ExternalAct.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)

    def parse_ExternalObservation(self, element: _Element):
        """Logical Model: ExternalObservation (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ExternalObservation.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)

    def parse_ExternalProcedure(self, element: _Element):
        """Logical Model: ExternalProcedure (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ExternalProcedure.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)

    def parse_ExternalDocument(self, element: _Element):
        """Logical Model: ExternalDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ExternalDocument.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)

    def parse_Precondition(self, element: _Element):
        """Logical Model: Precondition (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Precondition.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}criterion":
                    self.parse_Criterion(child)

    def parse_Criterion(self, element: _Element):
        """Logical Model: Criterion (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Criterion.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}value":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "ED":
                            self.parse_ED(child)
                        case "CD":
                            self.parse_CD(child)
                        case "CV":
                            self.parse_CV(child)
                        case "CE":
                            self.parse_CE(child)
                        case "II":
                            self.parse_II(child)
                        case "TEL":
                            self.parse_TEL(child)
                        case "AD":
                            self.parse_AD(child)
                        case "EN":
                            self.parse_EN(child)
                        case "PQ":
                            self.parse_PQ(child)
                        case "TS":
                            self.parse_TS(child)
                        case "IVL_PQ":
                            self.parse_IVL_PQ(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "EIVL_TS":
                            self.parse_EIVL_TS(child)
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)

    def parse_Observation(self, element: _Element):
        """Logical Model: Observation (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Observation.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code" | "{urn:hl7-org:v3}targetSiteCode":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case (
                    "{urn:hl7-org:v3}priorityCode"
                    | "{urn:hl7-org:v3}interpretationCode"
                    | "{urn:hl7-org:v3}methodCode"
                ):
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}value":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "ED":
                            self.parse_ED(child)
                        case "CD":
                            self.parse_CD(child)
                        case "CV":
                            self.parse_CV(child)
                        case "CE":
                            self.parse_CE(child)
                        case "II":
                            self.parse_II(child)
                        case "TEL":
                            self.parse_TEL(child)
                        case "AD":
                            self.parse_AD(child)
                        case "EN":
                            self.parse_EN(child)
                        case "PQ":
                            self.parse_PQ(child)
                        case "TS":
                            self.parse_TS(child)
                        case "IVL_PQ":
                            self.parse_IVL_PQ(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "EIVL_TS":
                            self.parse_EIVL_TS(child)
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)
                case "{urn:hl7-org:v3}referenceRange":
                    for rr_child in child:
                        match rr_child.tag:
                            case "{urn:hl7-org:v3}observationRange":
                                self.parse_ObservationRange(rr_child)

    def parse_ObservationRange(self, element: _Element):
        """Logical Model: ObservationRange (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ObservationRange.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}value":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "ED":
                            self.parse_ED(child)
                        case "CD":
                            self.parse_CD(child)
                        case "CV":
                            self.parse_CV(child)
                        case "CE":
                            self.parse_CE(child)
                        case "II":
                            self.parse_II(child)
                        case "TEL":
                            self.parse_TEL(child)
                        case "AD":
                            self.parse_AD(child)
                        case "EN":
                            self.parse_EN(child)
                        case "PQ":
                            self.parse_PQ(child)
                        case "TS":
                            self.parse_TS(child)
                        case "IVL_PQ":
                            self.parse_IVL_PQ(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "EIVL_TS":
                            self.parse_EIVL_TS(child)
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)
                case "{urn:hl7-org:v3}interpretationCode":
                    self.parse_CE(child)

    def parse_ObservationMedia(self, element: _Element):
        """Logical Model: ObservationMedia (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ObservationMedia.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}value":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_Organizer(self, element: _Element):
        """Logical Model: Organizer (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Organizer.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}priorityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)
                case "{urn:hl7-org:v3}component":
                    self.parse_OrganizerComponent(child)

    def parse_OrganizerComponent(self, element: _Element):
        """Logical Model: OrganizerComponent (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-OrganizerComponent.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}act":
                    self.parse_Act(child)
                case "{urn:hl7-org:v3}observation":
                    self.parse_Observation(child)
                case "{urn:hl7-org:v3}observationMedia":
                    self.parse_ObservationMedia(child)
                case "{urn:hl7-org:v3}organizer":
                    self.parse_Organizer(child)
                case "{urn:hl7-org:v3}procedure":
                    self.parse_Procedure(child)
                case "{urn:hl7-org:v3}regionOfInterest":
                    self.parse_RegionOfInterest(child)
                case "{urn:hl7-org:v3}substanceAdministration":
                    self.parse_SubstanceAdministration(child)
                case "{urn:hl7-org:v3}supply":
                    self.parse_Supply(child)

    def parse_Procedure(self, element: _Element):
        """Logical Model: Procedure (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Procedure.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case (
                    "{urn:hl7-org:v3}code"
                    | "{urn:hl7-org:v3}approachSiteCode"
                    | "{urn:hl7-org:v3}targetSiteCode"
                ):
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}priorityCode" | "{urn:hl7-org:v3}methodCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_RegionOfInterest(self, element: _Element):
        """Logical Model: RegionOfInterest (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RegionOfInterest.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_SubstanceAdministration(self, element: _Element):
        """Logical Model: SubstanceAdministration (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SubstanceAdministration.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code" | "{urn:hl7-org:v3}approachSiteCode":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "SXCM_TS" | None:
                            self.parse_SXCM_TS(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "EIVL_TS":
                            self.parse_EIVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)
                case (
                    "{urn:hl7-org:v3}priorityCode"
                    | "{urn:hl7-org:v3}routeCode"
                    | "{urn:hl7-org:v3}administrationUnitCode"
                ):
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}doseQuantity":
                    self.parse_IVL_PQ(child)
                case "{urn:hl7-org:v3}rateQuantity":
                    self.parse_IVL_PQ(child)
                case "{urn:hl7-org:v3}maxDoseQuantity":
                    self.parse_RTO_PQ_PQ(child)
                case "{urn:hl7-org:v3}consumable":
                    for c_child in child:
                        match c_child.tag:
                            case "{urn:hl7-org:v3}manufacturedProduct":
                                self.parse_ManufacturedProduct(c_child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)

    def parse_SXCM_TS(self, element: _Element):
        """Logical Model: SXCM_TS: GeneralTimingSpecification (V3 Data Type) ( Abstract ).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXCM_TS.html
        """
        for attribute in element.attrib:
            match attribute:
                case "value":
                    self.parse_TS(element)

    def parse_RTO_PQ_PQ(self, element: _Element):
        """Logical Model: RTO_PQ_PQ: Ratio (V3 Data Type) .

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RTO_PQ_PQ.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}numerator" | "{urn:hl7-org:v3}denominator":
                    self.parse_PQ(child)

    def parse_ManufacturedProduct(self, element: _Element):
        """Logical Model: ManufacturedProduct (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ManufacturedProduct.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}identifiedBy":
                    self.parse_IdentifiedBy(child)

    def parse_Supply(self, element: _Element):
        """Logical Model: Supply (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Supply.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}code":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    match child.get("{http://www.w3.org/2001/XMLSchema-instance}type"):
                        case "SXCM_TS" | None:
                            self.parse_SXCM_TS(child)
                        case "IVL_TS":
                            self.parse_IVL_TS(child)
                        case "EIVL_TS":
                            self.parse_EIVL_TS(child)
                        case "PIVL_TS":
                            self.parse_PIVL_TS(child)
                        case "SXPR_TS":
                            self.parse_SXPR_TS(child)
                case "{urn:hl7-org:v3}priorityCode":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}quantity":
                    self.parse_PQ(child)
                case "{urn:hl7-org:v3}expectedUseTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}product":
                    for p_child in child:
                        match p_child.tag:
                            case "{urn:hl7-org:v3}manufacturedProduct":
                                self.parse_ManufacturedProduct(p_child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                case "{urn:hl7-org:v3}specimen":
                    self.parse_Specimen(child)
                case "{urn:hl7-org:v3}performer":
                    self.parse_Performer2(child)
                case "{urn:hl7-org:v3}author":
                    self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}participant":
                    self.parse_Participant2(child)
                case "{urn:hl7-org:v3}entryRelationship":
                    self.parse_EntryRelationship(child)
                case "{urn:hl7-org:v3}reference":
                    self.parse_Reference(child)
                case "{urn:hl7-org:v3}precondition":
                    self.parse_Precondition(child)
