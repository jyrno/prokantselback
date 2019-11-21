from enum import Enum


class Type(str, Enum):
    PARONUUM            = 'PARONUUM'
    NOMINALISATSIOON    = 'NOMINALISATSIOON'
    POOLT_TARIND        = 'POOLT_TARIND'
    OLEMA_KESKSONA      = 'OLEMA_KESKSONA'
    KANTSELIIT          = 'KANTSELIIT'
    LIIGNE_MITMUS       = 'LIIGNE_MITMUS'
    SAAV_KAANE          = 'SAAV_KAANE'
    LT_MAARSONA         = 'LT_MAARSONA'
