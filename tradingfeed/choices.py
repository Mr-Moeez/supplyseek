# choices.py

from django.utils.translation import gettext_lazy as _


# choices.py


class Choices:
    # Type Choices for Alerts
    WTS = "WTS"
    WTB = "WTB"
    ALL = "ALL"
    ALERT_TYPE_CHOICES = [
        (WTS, "WTS"),
        (WTB, "WTB"),
        (ALL, "ALL"),
    ]

    ASAP = "ASAP"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    FREQUENCY_CHOICE = [
        (ASAP, "ASAP"),
        (DAILY, "DAILY"),
        (WEEKLY, "WEEKLY"),
        (MONTHLY, "MONTHLY"),
    ]

    # Condition Choices
    NEW = "NEW"
    USED = "USED"
    ALL = "ALL"
    CONDITION_CHOICES = [
        (NEW, "NEW"),
        (USED, "USED"),
        (ALL, "ALL"),
    ]

    # Currency Choices
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    AED = "AED"
    HKD = "HKD"
    CURRENCY_CHOICES = [
        (EUR, "EUR"),
        (USD, "USD"),
        (GBP, "GBP"),
        (AED, "AED"),
        (HKD, "HKD"),
    ]

    # Category Choices
    ELECTRONICS = "Electronics"
    ARCADE_EQUIPMENT = "Arcade Equipment"
    AUDIO = "Audio"
    CIRCUIT_BOARDS_COMPONENTS = "Circuit Boards & Components"
    COMMUNICATIONS = "Communications"
    COMPONENTS = "Components"
    COMPUTERS = "Computers"
    ELECTRONICS_ACCESSORIES = "Electronics Accessories"
    GPS_ACCESSORIES = "GPS Accessories"

    CATEGORY_CHOICES = [
        (ELECTRONICS, "Electronics"),
        (ARCADE_EQUIPMENT, "Arcade Equipment"),
        (AUDIO, "Audio"),
        (CIRCUIT_BOARDS_COMPONENTS, "Circuit Boards & Components"),
        (COMMUNICATIONS, "Communications"),
        (COMPONENTS, "Components"),
        (COMPUTERS, "Computers"),
        (ELECTRONICS_ACCESSORIES, "Electronics Accessories"),
        (GPS_ACCESSORIES, "GPS Accessories"),
    ]

    # Type Choices for Broadcast
    DISTRIBUTOR = "Distributor"
    TRADER = "Trader"
    WHOLESALER = "Wholesaler"
    OTHER = "Other"
    BROADCAST_TYPE_CHOICES = [
        (DISTRIBUTOR, "Distributor"),
        (TRADER, "Trader"),
        (WHOLESALER, "Wholesaler"),
        (OTHER, "Other"),
    ]

    # Status Choices
    ACTIVE = "active"
    INACTIVE = "inactive"
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    ]

    BASIC = "Basic"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"

    PLAN_CHOICES = [
        (BASIC, "Basic"),
        (PREMIUM, "Premium"),
        (ENTERPRISE, "Enterprise"),
    ]
