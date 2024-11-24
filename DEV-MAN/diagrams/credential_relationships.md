# Credential & Service Relationships

```mermaid
graph TD
    subgraph Email_Accounts[Email & Communication]
        Gmail[Gmail Primary]
        LHB[LHB Email]
        AIREI[AIREI Email]
        Ops[Operations Email]
        Callers[Cold Caller Emails]
    end

    subgraph CRM_Marketing[CRM & Marketing]
        GHL[GoHighLevel]
        MailGun[MailGun]
        Twilio[Twilio]
        BatchDialer[Batch Dialer]
        CallTools[Call Tools]
    end

    subgraph AI_Development[AI & Development]
        OpenAI[OpenAI]
        GitHub[GitHub]
        Docker[Docker]
        Claude[Claude]
        HuggingFace[Hugging Face]
    end

    subgraph Property_Tools[Property Systems]
        PropStream[PropStream]
        Zillow[Zillow]
        BatchLeads[Batch Leads]
        REISift[REI Sift]
    end

    subgraph Automation[Automation Tools]
        Zapier[Zapier]
        AutoGen[AutoGen]
        CrewAI[CrewAI]
        SuperAGI[SuperAGI]
    end

    % Email Connections
    Gmail --> GHL
    LHB --> MailGun
    AIREI --> Twilio

    % CRM Connections
    GHL --> Zapier
    MailGun --> Zapier
    Twilio --> GHL

    % AI Tool Connections
    OpenAI --> CrewAI
    OpenAI --> AutoGen
    GitHub --> Docker

    % Property Tool Connections
    PropStream --> REISift
    BatchLeads --> GHL
    
    % Automation Flows
    Zapier --> GHL
    Zapier --> MailGun
    CrewAI --> OpenAI
    AutoGen --> OpenAI

    classDef primary fill:#a7f3d0,stroke:#059669
    classDef secondary fill:#fef3c7,stroke:#d97706
    classDef aiTools fill:#e0e7ff,stroke:#4f46e5

    class Gmail,LHB,AIREI primary
    class GHL,OpenAI,GitHub primary
    class Zapier,CrewAI,AutoGen aiTools
```

## Service Categories

1. **Email & Communication**
   - Primary Business Accounts
   - Team Operation Accounts
   - Marketing Accounts

2. **CRM & Marketing**
   - Lead Management
   - Email Marketing
   - Phone Systems

3. **AI & Development**
   - AI Services
   - Code Repositories
   - Development Tools

4. **Property Systems**
   - Lead Generation
   - Property Analysis
   - Deal Management

5. **Automation Tools**
   - Workflow Automation
   - AI Agents
   - Integration Tools 