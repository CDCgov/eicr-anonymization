"""Parse for stepping through XML elements of a CDA document to collect sensitive elements and safe text."""  # noqa: E501

from lxml.etree import _Element


def track_path(element_type: str):
    """Track the current path in the XML document."""

    def decorator_track_path(func):
        def wrapper(self, element: _Element):
            """Track the path."""
            self.current_path.append(element_type)
            try:
                return func(self, element)
            finally:
                self.current_path.pop()

        return wrapper

    return decorator_track_path


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

    def __init__(self, element: _Element, cda_type: str, type_path: list[str] | None = None):
        """Initialize the Element with its attributes and text content."""
        self.name = element.tag

        self.attributes = {}
        for attribute in element.items():
            self.attributes[attribute[0]] = attribute[1]
        self.cda_type = cda_type
        self.text = element.text
        self.path = element.getroottree().getpath(element)
        self.line = element.sourceline
        self.type_path = "/".join(type_path) if type_path else None

    def __repr__(self) -> str:
        """Get a string representation of the tag."""
        root_tag = str(self.name).removeprefix("{urn:hl7-org:v3}")
        if self.type_path:
            repr = f"{self.line}, {self.type_path}: <{root_tag}"
        else:
            repr = f"{self.line}, {self.cda_type}: <{root_tag}"
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
        self.safe_text: set[str] = set()
        self.current_path: list[str] = []

    def collect_sensitive_elements_and_safe_words(self, element: _Element):
        """Find sensitive elements in the XML document.

        Args:
            element: The XML element to parse.
        """
        if element.tag == "{urn:hl7-org:v3}ClinicalDocument":
            self.parse_ClinicalDocument(element)
        else:
            raise ValueError(f"Unknown root element: {element.tag}")

        return self.sensitive_elements, self.safe_text

    def add_sensitive_element(self, element: _Element, cda_type: str):
        """Add a sensitive element to the list."""
        self.sensitive_elements.append(Element(element, cda_type, self.current_path))

    def add_safe_text(self, text: str):
        """Add a safe text element to the list."""
        self.safe_text.add(text)

    def parse_ClinicalDocument(self, element: _Element):
        """Logical Model: ClinicalDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ClinicalDocument.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}code" | "{urn:hl7-org:v3}confidentialityCode":
                #     self.parse_CE(child)
                # case "{urn:hl7-org:v3}effectiveTime":
                #     self.parse_TS(child)
                case "{urn:hl7-org:v3}recordTarget":
                    # Relevant for patient information
                    self.parse_RecordTarget(child)
                # case "{urn:hl7-org:v3}author":
                #     self.parse_Author(child)
                # case "{urn:hl7-org:v3}dataEnterer":
                #     self.parse_DataEnterer(child)
                # case "{urn:hl7-org:v3}informant":
                #     self.parse_Informant(child)
                # case "{urn:hl7-org:v3}custodian":
                #     self.parse_Custodian(child)
                # case "{urn:hl7-org:v3}informationRecipient":
                #     self.parse_InformationRecipient(child)
                # case "{urn:hl7-org:v3}authenticator":
                #     self.parse_Authenticator(child)
                # case "{urn:hl7-org:v3}participant":
                #     self.parse_Participant1(child)
                # case "{urn:hl7-org:v3}inFulfillmentOf":
                #     self.parse_InFulfillmentOf(child)
                # case "{urn:hl7-org:v3}documentationOf":
                #     self.parse_DocumentationOf(child)
                # case "{urn:hl7-org:v3}relatedDocument":
                #     self.parse_RelatedDocument(child)
                # case "{urn:hl7-org:v3}authorization":
                #     self.parse_Authorization(child)
                case "{urn:hl7-org:v3}componentOf":
                    self.parse_ComponentOf(child)
                case "{urn:hl7-org:v3}component":
                    self.parse_Component(child)

    @track_path("CE")
    def parse_CE(self, element: _Element):
        """Logical Model: CE: CodedWithEquivalents (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CE.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "displayName" | "codeSystemName":
                    self.add_safe_text(atribute[1])
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}originalText":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}translation":
                    self.parse_CD(child)
                case "{urn:hl7-org:v3}effectiveTime" | "{urn:hl7-org:v3}copyTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}RecordTarget":
                    self.parse_RecordTarget(child)

    @track_path("ED")
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

    @track_path("TEL")
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

    @track_path("IVL_TS")
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

    @track_path("IVXB_TS")
    def parse_IVXB_TS(self, element: _Element):
        """Logical Model: IVXB_TS: Interval Boundary PointInTime (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "IVXB_TS")

    @track_path("TS")
    def parse_TS(self, element: _Element):
        """Logical Model: TS: PointInTime (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-TS.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "TS")

    @track_path("PQ")
    def parse_PQ(self, element: _Element):
        """Parse a PQ (Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}translation":
                    self.parse_PQR(child)

    @track_path("PQR")
    def parse_PQR(self, element: _Element):
        """Handle a PQR (Quantity Range) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}originalText":
                    self.parse_ED(child)

    @track_path("EIVL_TS")
    def parse_EIVL_TS(self, element: _Element):
        """Parse an EIVL_TS (Explicit Interval Timestamp) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}event":
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}offset":
                    self.parse_IVL_PQ(child)

    @track_path("IVL_PQ")
    def parse_IVL_PQ(self, element: _Element):
        """Parse an IVL_PQ (Interval Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}low" | "{urn:hl7-org:v3}high":
                    self.parse_IVXB_PQ(child)
                case "{urn:hl7-org:v3}center" | "{urn:hl7-org:v3}width":
                    self.parse_PQ(child)

    @track_path("IVXB_PQ")
    def parse_IVXB_PQ(self, element: _Element):
        """Parse an IVXB_PQ (Interval Bound Quantity) XML element."""
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}translation":
                    self.parse_PQR(child)

    @track_path("PIVL_TS")
    def parse_PIVL_TS(self, element: _Element):
        """Parse a PIVL_TS (Periodic Interval Timestamp) XML element."""
        # PIVL_TS should not have a value attribute, however the 3.1 example eICR has it
        for atribute in element.items():
            match atribute[0]:
                case "value":
                    self.add_sensitive_element(element, "PIVL_TS")
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}phase":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}period":
                    self.parse_PQ(child)

    @track_path("SXPR_TS")
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

    @track_path("CD")
    def parse_CD(self, element: _Element):
        """Logical Model: CD: ConceptDescriptor (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CD.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "displayName" | "codeSystemName":
                    self.add_safe_text(atribute[1])
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}originalText":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}qualifier":
                    self.parse_CR(child)
                case "{urn:hl7-org:v3}translation":
                    self.parse_CD(child)

    @track_path("CR")
    def parse_CR(self, element: _Element):
        """Logical Model: CR: ConceptRole (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CR.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}value":
                    self.parse_CD(child)

    @track_path("RecordTarget")
    def parse_RecordTarget(self, element: _Element):
        """Logical Model: RecordTarget (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RecordTarget.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}patientRole":
                    # Relevant for patient information
                    self.parse_PatientRole(child)

    @track_path("PatientRole")
    def parse_PatientRole(self, element: _Element):
        """Logical Model: PatientRole (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PatientRole.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}addr":
                    # Relevant for patient address
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    # I assume patient contact inform will need to be anonymized
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}patient":
                    # Relevant for patient information
                    self.parse_Patient(child)
                case "{urn:hl7-org:v3}providerOrganization":
                    self.parse_Organization(child)

    @track_path("II")
    def parse_II(self, element: _Element):
        """Logical Model: II: InstanceIdentifier (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-II.html
        """
        for atribute in element.items():
            match atribute[0]:
                case "extension":
                    self.add_sensitive_element(element, "II")

    @track_path("IdentifiedBy")
    def parse_IdentifiedBy(self, element: _Element):
        """Logical Model: IdentifiedBy (CDA Class) ( Abstract ).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IdentifiedBy.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}alterateIdentification":
                    self.parse_AlternateIdentification(child)

    @track_path("AlternateIdentification")
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

    @track_path("AD")
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

    @track_path("ADXP")
    def parse_ADXP(self, element: _Element):
        """Logical Model: ADXP: CharacterString (V3 Data Type) .

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ADXP.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "ADXP")

    @track_path("Patient")
    def parse_Patient(self, element: _Element):
        """Logical Model: Patient (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Patient.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}id":
                    self.parse_II(child)
                case "{urn:hl7-org:v3}name":
                    # Patient name
                    self.parse_PN(child)
                case (
                    "{urn:hl7-org:v3}administrativeGenderCode"
                    | "{urn:hl7-org:v3}materialStatusCode"
                    | "{urn:hl7-org:v3}religiousAffiliationCode"
                    | "{urn:hl7-org:v3}raceCode"
                    | "{urn:hl7-org:v3}ethnicGroupCode"
                    | "{urn:hl7-org:v3}languageCommunication"
                ):
                    # Will need to pull out ethnicty and race
                    self.parse_CE(child)
                case "{urn:hl7-org:v3}birthTime" | "{urn:hl7-org:v3}deceasedTime":
                    # Patient dates
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}desc":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}guardian":
                    self.parse_Guardian(child)
                case "{urn:hl7-org:v3}birthplace":
                    self.parse_Birthplace(child)

    @track_path("PN")
    def parse_PN(self, element: _Element):
        """Logical Model: PN: PersonName (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PN.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "PN")
        for child in element:
            match child.tag:
                case (
                    "{urn:hl7-org:v3}family" | "{urn:hl7-org:v3}given"
                    # | "{urn:hl7-org:v3}prefix"
                    # | "{urn:hl7-org:v3}suffix"
                ):
                    self.parse_ENXP(child)
                case "{urn:hl7-org:v3}validTime":
                    self.parse_IVL_TS(child)

    @track_path("ENXP")
    def parse_ENXP(self, element: _Element):
        """Logical Model: ENXP: Entity Name Part (V3 Data Type).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ENXP.html
        """
        if has_text(element):
            self.add_sensitive_element(element, "ENXP")

    @track_path("Guardian")
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

    @track_path("Person")
    def parse_Person(self, element: _Element):
        """Logical Model: Person (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Person.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                # case "{urn:hl7-org:v3}asPatientRelationship":
                #     self.parse_CE(child)

    @track_path("Birthplace")
    def parse_Birthplace(self, element: _Element):
        """Logical Model: Birthplace (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Birthplace.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}place":
                    self.parse_Place(child)

    @track_path("Place")
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

    @track_path("EN")
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

    @track_path("Organization")
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

    @track_path("ON")
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

    @track_path("OrganizationPartOf")
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

    @track_path("Author")
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

    @track_path("AssignedAuthor")
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

    @track_path("AuthoringDevice")
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

    @track_path("MaintainedEntity")
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

    @track_path("DataEnterer")
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

    @track_path("AssignedEntity")
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

    @track_path("Informant")
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

    @track_path("RelatedEntity")
    def parse_RelatedEntity(self, element: _Element):
        """Logical Model: RelatedEntity (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedEntity.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}code":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                case "{urn:hl7-org:v3}relatedPerson":
                    self.parse_Person(child)

    @track_path("Custodian")
    def parse_Custodian(self, element: _Element):
        """Logical Model: Custodian (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Custodian.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}assignedCustodian":
                    self.parse_AssignedCustodian(child)

    @track_path("AssignedCustodian")
    def parse_AssignedCustodian(self, element: _Element):
        """Logical Model: AssignedCustodian (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedCustodian.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}representedCustodianOrganization":
                    self.parse_CustodianOrganization(child)

    @track_path("CustodianOrganization")
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

    @track_path("InformationRecipient")
    def parse_InformationRecipient(self, element: _Element):
        """Logical Model: InformationRecipient (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InformationRecipient.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}intendedRecipient":
                    self.parse_IntendedRecipient(child)

    @track_path("IntendedRecipient")
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

    @track_path("Authenticator")
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

    @track_path("Participant1")
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

    @track_path("AssociatedEntity")
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

    @track_path("InFulfillmentOf")
    def parse_InFulfillmentOf(self, element: _Element):
        """Logical Model: InFulfillmentOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InFulfillmentOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}order":
                    self.parse_Order(child)

    @track_path("Order")
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

    @track_path("DocumentationOf")
    def parse_DocumentationOf(self, element: _Element):
        """Logical Model: DocumentationOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-DocumentationOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}serviceEvent":
                    self.parse_ServiceEvent(child)

    @track_path("ServiceEvent")
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

    @track_path("Performer1")
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

    @track_path("RelatedDocument")
    def parse_RelatedDocument(self, element: _Element):
        """Logical Model: RelatedDocument (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedDocument.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}parentDocument":
                    self.parse_ParentDocument(child)

    @track_path("ParentDocument")
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

    @track_path("Authorization")
    def parse_Authorization(self, element: _Element):
        """Logical Model: Authorization (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Authorization.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}consent":
                    self.parse_Consent(child)

    @track_path("Consent")
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

    @track_path("ComponentOf")
    def parse_ComponentOf(self, element: _Element):
        """Logical Model: ComponentOf (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ComponentOf.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}encompassingEncounter":
                    self.parse_EncompassingEncounter(child)

    @track_path("EncompassingEncounter")
    def parse_EncompassingEncounter(self, element: _Element):
        """Logical Model: EncompassingEncounter (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EncompassingEncounter.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}id":
                #     self.parse_II(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                # case (
                #     "{urn:hl7-org:v3}admissionReferralSourceCode"
                #     | "{urn:hl7-org:v3}dischargeDispositionCode"
                # ):
                #     self.parse_CE(child)
                # case "{urn:hl7-org:v3}responsibleParty":
                #     for rp_child in child:
                #         match rp_child.tag:
                #             case "{urn:hl7-org:v3}assignedEntity":
                #                 self.parse_AssignedEntity(rp_child)
                # case "{urn:hl7-org:v3}encounterParticipant":
                #     self.parse_EncounterParticipant(child)
                # case "{urn:hl7-org:v3}location":
                #     for ep_child in child:
                #         match ep_child.tag:
                #             case "{urn:hl7-org:v3}healthCareFacility":
                #                 self.parse_HealthCareFacility(ep_child)

    @track_path("EncounterParticipant")
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

    @track_path("HealthCareFacility")
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

    @track_path("Component")
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

    @track_path("NonXMLBody")
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

    @track_path("StructuredBody")
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

    @track_path("Section")
    def parse_Section(self, element: _Element):
        """Logical Model: Section (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Section.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}id":
                #     self.parse_II(child)
                # case "{urn:hl7-org:v3}code":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_xhtml(child)
                # case "{urn:hl7-org:v3}confidentialityCode":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_Subject(child)
                # case "{urn:hl7-org:v3}author":
                #     self.parse_Author(child)
                case "{urn:hl7-org:v3}informant":
                    self.parse_Informant(child)
                case "{urn:hl7-org:v3}entry":
                    self.parse_Entry(child)
                case "{urn:hl7-org:v3}component":
                    for c_child in child:
                        match c_child.tag:
                            case "{urn:hl7-org:v3}section":
                                self.parse_Section(c_child)

    @track_path("xhtml")
    def parse_xhtml(self, element: _Element):
        """XHTML Content.

        https://hl7.org/fhir/R5/narrative.html#xhtml
        """
        self.add_sensitive_element(element, "xhtml")

    @track_path("Subject")
    def parse_Subject(self, element: _Element):
        """Logical Model: Subject (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Subject.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}awarenessCode":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}relatedSubject":
                    self.parse_RelatedSubject(child)

    @track_path("RelatedSubject")
    def parse_RelatedSubject(self, element: _Element):
        """Logical Model: RelatedSubject (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedSubject.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}code":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}addr":
                    self.parse_AD(child)
                case "{urn:hl7-org:v3}telecom":
                    self.parse_TEL(child)
                case "{urn:hl7-org:v3}subject":
                    self.parse_SubjectPerson(child)

    @track_path("SubjectPerson")
    def parse_SubjectPerson(self, element: _Element):
        """Logical Model: SubjectPerson (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SubjectPerson.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}name":
                    self.parse_PN(child)
                # case "{urn:hl7-org:v3}desc":
                #     self.parse_ED(child)
                # case "{urn:hl7-org:v3}administrativeGenderCode":
                #     self.parse_CE(child)
                case "{urn:hl7-org:v3}birthTime":
                    self.parse_TS(child)
                case "{urn:hl7-org:v3}deceasedTime":
                    self.parse_TS(child)

    @track_path("Entry")
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

    @track_path("Act")
    def parse_Act(self, element: _Element):
        """Logical Model: Act (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Act.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}id":
                #     self.parse_II(child)
                # case "{urn:hl7-org:v3}code":
                #     self.parse_CD(child)
                case "{urn:hl7-org:v3}text":
                    self.parse_ED(child)
                case "{urn:hl7-org:v3}effectiveTime":
                    self.parse_IVL_TS(child)
                # case "{urn:hl7-org:v3}priorityCode":
                #     self.parse_CE(child)
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

    @track_path("Specimen")
    def parse_Specimen(self, element: _Element):
        """Logical Model: Specimen (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Specimen.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}specimenRole":
                    self.parse_SpecimenRole(child)

    @track_path("SpecimenRole")
    def parse_SpecimenRole(self, element: _Element):
        """Logical Model: SpecimenRole (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SpecimenRole.html
        """
        for child in element:
            match child.tag:
                # case "{urn:hl7-org:v3}id":
                #     self.parse_II(child)
                # case "{urn:hl7-org:v3}identifiedBy":
                #     self.parse_IdentifiedBy(child)
                case "{urn:hl7-org:v3}specimenPlayingEntity":
                    self.parse_PlayingEntity(child)

    @track_path("PlayingEntity")
    def parse_PlayingEntity(self, element: _Element):
        """Logical Model: SpecimenPlayingEntity (CDA Class).

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

    @track_path("Performer2")
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

    @track_path("Participant2")
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

    @track_path("ParticipantRole")
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

    @track_path("Device")
    def parse_Device(self, element: _Element):
        """Logical Model: Device (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Device.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}code":
                    self.parse_CE(child)

    @track_path("Entity")
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

    @track_path("EntryRelationship")
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

    @track_path("Encounter")
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

    @track_path("Reference")
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

    @track_path("ExternalAct")
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

    @track_path("ExternalObservation")
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

    @track_path("ExternalProcedure")
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

    @track_path("ExternalDocument")
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

    @track_path("Precondition")
    def parse_Precondition(self, element: _Element):
        """Logical Model: Precondition (CDA Class).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Precondition.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}criterion":
                    self.parse_Criterion(child)

    @track_path("Criterion")
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

    @track_path("Observation")
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

    @track_path("ObservationRange")
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

    @track_path("ObservationMedia")
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

    @track_path("Organizer")
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

    @track_path("OrganizerComponent")
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

    @track_path("Procedure")
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

    @track_path("RegionOfInterest")
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

    @track_path("SubstanceAdministration")
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

    @track_path("SXCM_TS")
    def parse_SXCM_TS(self, element: _Element):
        """Logical Model: SXCM_TS: GeneralTimingSpecification (V3 Data Type) ( Abstract ).

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXCM_TS.html
        """
        for attribute in element.attrib:
            match attribute:
                case "value":
                    self.parse_TS(element)

    @track_path("RTO_PQ_PQ")
    def parse_RTO_PQ_PQ(self, element: _Element):
        """Logical Model: RTO_PQ_PQ: Ratio (V3 Data Type) .

        https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RTO_PQ_PQ.html
        """
        for child in element:
            match child.tag:
                case "{urn:hl7-org:v3}numerator" | "{urn:hl7-org:v3}denominator":
                    self.parse_PQ(child)

    @track_path("ManufacturedProduct")
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

    @track_path("Supply")
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
